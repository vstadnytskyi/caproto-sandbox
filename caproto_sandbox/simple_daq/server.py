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
        self.daq.io_push_queue = self.io_push_queue
        self.daq.io_pull_queue = self.io_pull_queue

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



if __name__ == '__main__':
    from  caproto_sandbox.simple_daq.driver import Driver
    from  caproto_sandbox.simple_daq.device import Device


    driver = Driver()
    device = Device()
    device.start()
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='simple_dl:',
        desc=dedent(Server.__doc__))
    ioc = Server(**ioc_options)
    run(ioc.pvdb, **run_options)
