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
        from circular_buffer_numpy import circular_buffer
        self.buffer = circular_buffer.CircularBuffer(shape = (1000,4))
        self.dt = 1
        self.running = True
        self.header = ['time','cpu','memory','battery']
        self.io_push_queue = None
        self.io_put_queue = None
        self.driver = driver

    def run_once(self):
        arr = self.driver.read()
        self.buffer.append(arr)

        io_dict = {}
        io_dict['TIME'] = arr[0,0]
        io_dict['CPU'] = arr[0,1]
        io_dict['MEMORY'] = arr[0,2]
        io_dict['BATTERY'] = arr[0,3]
        io_dict['LIST'] = [arr[0,0],arr[0,1],arr[0,2],arr[0,3]]
        self.io_push(io_dict)

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



if __name__ == '__main__':
    from caproto_sandbox.simple_daq.driver import Driver
    driver = Driver()
    device = Device(driver = driver)
    device.start()
