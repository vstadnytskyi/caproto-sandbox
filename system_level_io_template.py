#!/usr/bin/env python3
import termios
import fcntl
import sys
import os
import threading
import atexit
import time
from datetime import datetime
import itertools
from logging import debug,info,warn,error
#Input/Output server library
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run


class SystemLevelIOTemplate(PVGroup):
    CMD = pvproperty(value='This is command PV', max_length=1000, dtype=str)
    ACK = pvproperty(value='This is acknowledgement PV', max_length=1000, dtype=str, read_only = True)

    device = None

    # NOTE the decorator used here:
    @CMD.startup
    async def RBV(self, instance, async_lib):
        # This method will be called when the server starts up.
        debug('* request method called at server startup')
        self.io_get_queue = async_lib.ThreadsafeQueue()
        self.io_put_queue = async_lib.ThreadsafeQueue()
        self.device.io_put_queue = self.io_put_queue
        self.device.io_get_queue = self.io_get_queue

        # Loop and grab items from the response queue one at a time
        while True:
            value = await self.io_put_queue.async_get()
            debug(f'Got put request from the device: {value}')
            if 'ACK' in list(value.keys()):
                await self.ACK.write(value['ACK'])
            elif 'CMD' in list(value.keys()):
                await self.CMD.write(value['CMD'])

    @CMD.putter
    async def VAL(self, instance, value):
        print('Received update for the {}, sending new value {}'.format('VAL',value))
        await self.device_ioexecute(pv_name = 'VAL', value = float(value))
        return value

    async def device_ioexecute(self, pv_name, value):
        """
        """
        if self.device is not None:
            self.device.ioexecute(pv_name = pv_name, value = value)

    async def device_ioread(self, pv_name, value):
        """
        """
        pass

    def update_pvs(self):
        """
        Force update of all PVs. Works only if self.device is assigned. If None, nothing will happen.
        """
        if self.device is not None:
            pass
        else:
            pass

def run_io(command, device):
    """

    """
    #from system level import System Level class
    from tempfile import gettempdir
    import logging
    logfile_name = 'syringe_pump_device_io.log'
    print(f"the location of the log file is {gettempdir()+'/' + logfile_name}")
    logging.basicConfig(filename=gettempdir()+'/'+logfile_name,
                        level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")
    debug('test write debug')
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='NIH:SYRINGE.',
        desc='Run an IOC that does blocking tasks on a worker thread.')

    ioc = Server(**ioc_options)
    ioc.device = device
    run(ioc.pvdb, **run_options)

def init_device():
    """
    initialize device and return device object
    """
    return None

def start_io_process(command = None, device = None):
    ""
    from syringe_pump import device_io
    import multiprocessing
    p = multiprocessing.Process(target=run_io,kwargs=({'command':command,'device':device))
    p.start()
    return p

if __name__ == '__main__':
    device = init_device()
    start_io_process(command = None, device = device)
