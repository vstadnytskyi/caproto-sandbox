#!/usr/bin/env python3
"""
Simple IOC based on caproto library.
It has
"""
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run
from textwrap import dedent
from pdb import pm

from numpy import random, array, zeros, ndarray, nan, isnan
from time import time, sleep, ctime



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

    MEMORY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = 'GB')

    BATTERY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = '%')

    TIME = pvproperty(value='time unknown', read_only = True, dtype = str)

    dt = pvproperty(value=1.0, precision = 3, units = 's')

    @CPU.startup
    async def CPU(self, instance, async_lib):
        """
        This method will be called when the server starts up and first initialization of PV with name CPU.
        """
        self.io_pull_queue = async_lib.ThreadsafeQueue()
        self.io_push_queue = async_lib.ThreadsafeQueue()
        self.device.io_push_queue = self.io_push_queue
        self.device.io_pull_queue = self.io_pull_queue

        # Loop and grab items from the response queue one at a time
        while True:
            io_dict = await self.io_push_queue.async_get()
            # Propagate the keypress to the EPICS PV, triggering any monitors
            # along the way
            for key in list(io_dict.keys()):
                if key == 'TIME':
                    await self.TIME.write(ctime(io_dict[key]))
                elif key == 'CPU':
                    await self.CPU.write(io_dict[key])
                elif key == 'MEMORY':
                    await self.MEMORY.write(io_dict[key]/1024/1024/1024)
                elif key == 'BATTERY':
                    await self.BATTERY.write(io_dict[key])
                elif key == 'dt':
                    await self.dt.write(io_dict[key])
    @dt.putter
    async def dt(self, instance, value):
        """
        this function is called everytime the value of dt is changed in the server's database, whether it is changed externally or internally.
        """
        print('Received update for the {}, sending new value {}'.format('dt',value))
        self.device.dt = value
        return value

def run_server(name = 'simple_daq'):
    from  caproto_sandbox.simple_daq.driver import Driver
    from  caproto_sandbox.simple_daq.device import Device
    from  caproto_sandbox.simple_daq.server import Server

    import sys
    print(sys.argv)
    sys.argv.append('--list-pvs')

    driver = Driver()
    device = Device(driver = driver)
    device.start()

    ioc_options, run_options = ioc_arg_parser(
        default_prefix=f'{name}:',
        desc=dedent(Server.__doc__))
    server = Server(**ioc_options)
    # pass the device instance into the server instance for bidirectional communication
    server.device = device

    run(server.pvdb, **run_options)

if __name__ == '__main__':
    from  caproto_sandbox.simple_daq.driver import Driver
    from  caproto_sandbox.simple_daq.device import Device
    import sys

    driver = Driver()
    device = Device(driver = driver)
    device.start()
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='simple_daq:',
        desc=dedent(Server.__doc__))
    server = Server(**ioc_options)
    # pass the device instance into the server instance for bidirectional communication
    server.device = device
    print(sys.argv)
    run(server.pvdb, **run_options)
