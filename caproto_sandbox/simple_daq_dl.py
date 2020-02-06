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

class DAQ(object):
    def __init__(self):
        from circular_buffer_numpy import circular_buffer
        self.buffer = circular_buffer.CircularBuffer(shape = (1000,4))
        self.dt = 0.05
        self.running = True
        self.header = ['time','cpu','memory','battery']
        self.io_push_queue = None
        self.io_put_queue = None

    def read(self):
        import psutil
        from numpy import zeros
        memory = psutil.virtual_memory().available
        cpu = psutil.cpu_percent()
        battery = psutil.sensors_battery().percent
        arr = zeros((1,4))
        arr[0,0] = time()
        arr[0,1] = cpu
        arr[0,2] = memory
        arr[0,3] = battery
        return arr

    def run_once(self):
        arr = self.read()
        self.buffer.append(arr)

        io_dict = {}
        io_dict['TIME'] = arr[0,0]
        io_dict['CPU'] = arr[0,1]
        io_dict['MEMORY'] = arr[0,2]
        io_dict['BATTERY'] = arr[0,3]
        io_dict['LIST'] = [arr[0,0],arr[0,1],arr[0,2],arr[0,3]]


        self.io_push(io_dict)
        sleep(self.dt)

    def run(self):
        from time import sleep
        self.running = True
        while self.running:
            self.run_once()
            sleep(self.dt)

    def start(self):
        from ubcs_auxiliary.multithreading import new_thread
        new_thread(self.run)

    def stop(self):
        self.running = False

    def set_dt(self,value):
        self.dt = value
    def get_dt(self):
        return self.dt

    def io_push(self,io_dict = None):
        if self.io_push_queue is not None:
            self.io_push_queue.put(io_dict)



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

    CPU = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1)
    MEMORY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1)
    BATTERY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1)
    TIME = pvproperty(value=time(), read_only = True, dtype = float, precision = 3)
    dt = pvproperty(value=1.0)
    LIST = pvproperty(value=[0.0,0.0,0.0,0.0])

    @CPU.startup
    async def CPU(self, instance, async_lib):
        # This method will be called when the server starts up.
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
                elif key == 'LIST':
                    await self.LIST.write(io_dict[key])



daq = DAQ()
daq.start()

if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='simple_dl:',
        desc=dedent(Server.__doc__))
    ioc = Server(**ioc_options)
    run(ioc.pvdb, **run_options)
