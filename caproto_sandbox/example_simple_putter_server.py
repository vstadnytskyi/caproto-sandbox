#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# In this example, we explore what is happening when a PV is updated internlly via write command or externally via client writing into PV.
#
# I suspect that in both cases the @putter funcion is getting executed.
#

from caproto.server import pvproperty, PVGroup, SubGroup, ioc_arg_parser, run
from caproto import ChannelType
from logging import debug, info, warning, error

from time import sleep
from tempfile import gettempdir
import os
from ubcs_auxiliary.saved_property import DataBase, SavedProperty

class Device():
    _bit = 0

    def __init__(self):
        pass

    def set_bit(self,value):
        print(f'bit set to {value}')
        self._bit = value
    def get_bit(self):
        return self._bit
    bit = property(get_bit,set_bit)

    def set_bit_client(self,value):
        print(f'bit set to {value} by client')
        self.bit = value

    def set_bit_server(self,value):
        print(f'bit set to {value} by server')
        self.io_put_queue.put({'bit':value})

class Server(PVGroup):
    io_put_queue = None
    device = None

    # DOWNSTREAM TABLE
    bit = pvproperty(value=0, dtype = bool)
    set_bit = pvproperty(value=0, dtype = bool)

    @bit.startup
    async def bit(self, instance, async_lib):
        self.io_put_queue = async_lib.ThreadsafeQueue()
        self.io_get_queue = async_lib.ThreadsafeQueue()
        if self.device is not None:
            self.device.io_put_queue = self.io_put_queue
            self.device.io_get_queue = self.io_get_queue

        while True:
            if True: #self.put_queue is not None:
                entry = await self.io_put_queue.async_get()
                print(f'Async Put Queue: Got put request from the device: {entry}')
                for key in entry.keys():
                    if key == 'bit':
                        print(f'got bit from io_put_queue with value {entry[key]}')
                        await self.bit.write(entry[key])
                    elif key == 'set_bit':
                        print(f'got bit from io_put_queue with value {entry[key]}')
                        self.device.set_bit_server(entry[key])

    @bit.putter
    async def bit(self, instance, value):
        """
        called when the a new value is written into "jog" PV
        """
        print(f"Server: {'bit'} Got 'put' request from outside: new value is {value} and type {type(value)}")
        if self.device is not None:
            self.device.set_bit_client(value)
        else:
            print('device is None')

    @set_bit.putter
    async def set_bit(self, instance, value):
        """
        called when the a new value is written into "jog" PV
        """
        print(f"Server: {'set_bit'} Got 'put' request from outside: new value is {value} and type {type(value)}")
        if self.device is not None:
            self.device.set_bit_server(value)
        else:
            print('device is None')

if __name__ == '__main__':
    device = Device()

    ioc_options, run_options = ioc_arg_parser(
        default_prefix='TEST:PUTTER.',
        desc='description')
    server  = Server(**ioc_options)
    server.device = device
    #start async caproto server IO
    run(server.pvdb, **run_options)
