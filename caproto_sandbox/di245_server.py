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

#Input/Output server library
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run

from numpy import zeros, random, nan


class Device(object):
    running = True
    def __init__(self):
        self.counter = 0
        self.update_time = 1
        self.io_put_queue = None
        self.io_pv_list = None
        self.io = None
    def init(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def run_once(self):
        self.counter += 1
        try:
            self.iowrite(pv_dict ={'counter':self.counter,'counter2':self.counter})
        except:
            print('ioc is not running yet')
        print('cycle: {}'.format(self.counter))

    def run(self):
        from time import sleep
        while self.running:
            self.run_once()
            sleep(self.update_time)

    def start(self):
        from ubcs_auxiliary.threading import start_new_safe_thread
        start_new_safe_thread(self.run)

    def stop(self):
        raise NotImplementedError

    def set_counter(self,value):
        self.counter = value

    def iowrite(self, pv_dict = None):
        """
    	put dictionary of key:value pairs to IO.

    	Parameters
    	----------
    	pv_dict:  (dictionary)
    		dictionary of PVs and new PV values

    	Returns
    	-------

    	Examples
    	--------
    	>>> device.ioput(pv_dict = {'running':True})

        """
        if self.io is not None:
            self.io.io_put_queue.put(pv_dict)
        else:
            print('no IO is linked to the device')

    def ioread(self, pv_name = ''):
        """
    	put dictionary of key:value pairs to IO.

    	Parameters
    	----------
    	pv_dict:  (dictionary)
    		dictionary of PVs and new PV values

    	Returns
    	-------

    	Examples
    	--------
    	>>> device.ioput(pv_dict = {'running':True})

        """
        raise NotImplementedError


class ServerIO(PVGroup):
    running = pvproperty(value=1)
    pressure_downstream = pvproperty(value=nan, units = 'atm', read_only = True)
    pressure_upstream = pvproperty(value=nan, units = 'atm', read_only = True)
    pressure_barometric = pvproperty(value=nan, units = '100kPa', read_only = True)
    temperature = pvproperty(value=nan, units = 'C', read_only = True)
    update_time = pvproperty(value=1.0, units = 'seconds')
    CB = pvproperty(value = [nan]*100, read_only = True)
    CMD = pvproperty(value = '')
    ACK = pvproperty(value = '')
    calibration = pvproperty(value = [1,1,1,1], read_only = True)
    Last_Experiment = pvproperty(value = [nan]*100, read_only = True)
    counter = pvproperty(value=nan, read_only = True)

    # NOTE the decorator used here:
    @running.startup
    async def running(self, instance, async_lib):
        # This method will be called when the server starts up.
        print('* request method called at server startup')
        self.io_get_queue = async_lib.ThreadsafeQueue()
        self.io_put_queue = async_lib.ThreadsafeQueue()
        device.io = self

        # Loop and grab items from the response queue one at a time
        while True:
            value = await self.io_put_queue.async_get()
            print(f'Got put request from the device: {value}')
            if 'counter' in list(value.keys()):
                await self.counter.write(value['counter'])

    @counter.putter
    async def counter(self, instance, value):
        print('Received update for the {}, sending new value {}'.format('counter',value))
        device.set_counter(value = value)
        return value

    @update_time.putter
    async def update_time(self, instance, value):
        print('Received update for the {}, sending new value {}'.format('update_time',value))
        device.update_time = value
        return value

class Client():
    pass

device = Device()
device.start()


if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='NIH:DI245.',
        desc='Run an IOC that does blocking tasks on a worker thread.')

    ioc = ServerIO(**ioc_options)
    run(ioc.pvdb, **run_options)
