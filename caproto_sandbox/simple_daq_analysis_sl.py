#!/usr/bin/env python3
"""
Simple IOC based on caproto library.
It has
"""
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run
import caproto
from textwrap import dedent
from pdb import pm

from numpy import random, array, zeros, ndarray, nan, isnan
from time import time,sleep
from pickle import dumps, loads

from circular_buffer_numpy import circular_buffer

class DAQ():

    def __init__(self):
        self.io_push_queue = None
        self.io_pull_queue = None
        self.dt = 0.1
        from caproto.threading.client import Context
        ctx = Context()
        record_name = 'simple_dl'
        self.lst, = ctx.get_pvs(f'{record_name}:LIST')

    def init(self):
        from caproto.threading.client import Context
        ctx = Context()
        record_name = 'simple_dl'
        self.lst,self.cpu = ctx.get_pvs(f'{record_name}:LIST',f'{record_name}:CPU')

    def io_pull(self):
        """
        """
        io_dict = {}
        if self.lst is not None:
            data = self.lst.read().data
            io_dict["TIME"] = data[0]
            io_dict["CPU"] = data[1]
            io_dict["MEMORY"] = data[2]/1024/1024/1024
            io_dict["BATTERY"] = data[3]
        return io_dict

    def io_push(self, io_dict):

        if self.io_push_queue is not None:
            self.io_push_queue.put(io_dict)

    def run(self):
        from time import time, sleep
        self.running = True
        while self.running:
            io_dict = self.io_pull()
            self.io_push(io_dict=io_dict)
            sleep(self.dt)

    def start(self):
        from ubcs_auxiliary.multithreading import new_thread
        new_thread(self.run)


class Server(PVGroup):
    """
    An IOC with three uncoupled read/writable PVs

    Scalar PVs
    ----------
    CPU
    MEMORY
    BATTERY

    Vectors PVs
    -----------

    """

    CPU = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = '%')
    MEMORY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 3, units = 'GB')
    BATTERY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = '%')
    TIME = pvproperty(value=time(), read_only = True, dtype = float, precision = 12, units = 's')
    dt = pvproperty(value=1.0)

    @CPU.startup
    async def CPU(self, instance, async_lib):
        # This method will be called when the server starts up.
        print('* request method called at server startup')
        self.io_pull_queue = async_lib.ThreadsafeQueue()
        self.io_push_queue = async_lib.ThreadsafeQueue()
        daq.io_push_queue = self.io_push_queue

        # Loop and grab items from the response queue one at a time
        while True:
            io_dict = await self.io_push_queue.async_get()
            # Propagate the keypress to the EPICS PV, triggering any monitors
            # along the way
            for key in list(io_dict.keys()):
                if key == 'TIME':
                    await self.TIME.write(io_dict[key])
                elif key == 'CPU':
                    await self.CPU.write(io_dict[key])
                elif key == 'MEMORY':
                    await self.MEMORY.write(io_dict[key])
                elif key == 'BATTERY':
                    await self.BATTERY.write(io_dict[key])


daq = DAQ()
daq.start()

if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='simple_sl:',
        desc=dedent(Server.__doc__))
    ioc = Server(**ioc_options)
    run(ioc.pvdb, **run_options)
