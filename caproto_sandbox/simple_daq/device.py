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

class Device(object):
    def __init__(self, driver):
        """
        initialization of the instance and creation of all other instances and variables
        """
        from circular_buffer_numpy.circular_buffer import CircularBuffer
        self.buffer = CircularBuffer(shape = (1000,4))
        self.dt = 1
        self.running = False
        self.header = ['time','cpu','memory','battery']
        self.io_push_queue = None
        self.io_put_queue = None
        self.driver = driver
        self.threads = {}

    def run_once(self):
        """
        the single execution of a code that later is looped in while running=true loop
        """
        #
        arr = self.driver.read()
        self.buffer.append(arr)

        #push to IO for publishing
        io_dict = {}
        io_dict['TIME'] = arr[0,0]
        io_dict['CPU'] = arr[0,1]
        io_dict['MEMORY'] = arr[0,2]
        io_dict['BATTERY'] = arr[0,3]
        io_dict['LIST'] = [arr[0,0],arr[0,1],arr[0,2],arr[0,3]]
        self.io_push(io_dict)

    def run(self):
        """
        while running = True loop that executes run_once() in a loop on a timer.
        """
        from time import sleep, time
        self.running = True
        while self.running:
            t1 = time()
            self.run_once()
            t2 = time()
            dt = t2-t1
            sleep(self.dt-dt)

    def start(self):
        """
        start the while running=True loop(function run()) in a separate thread.
        """
        from ubcs_auxiliary.multithreading import new_thread
        self.threads['running'] = new_thread(self.run)

    def stop(self):
        """
        stop the while running=True loop(function run()) in a separate thread.
        """
        self.running = False

    def set_dt(self,value):
        """
        wrapper to set dT
        """
        self.dt = value
    def get_dt(self):
        """
        wrapper to get dT
        """
        return self.dt

    def io_push(self,io_dict = None):
        """
        wrapper to push the updates into CA server for further publishing on the network.
        """
        if self.io_push_queue is not None:
            self.io_push_queue.put(io_dict)



if __name__ == '__main__':
    from caproto_sandbox.simple_daq.driver import Driver
    driver = Driver()
    device = Device(driver = driver)
    device.start()
