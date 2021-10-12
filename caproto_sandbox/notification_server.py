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

import socket

ip_address = socket.gethostbyname(socket.gethostname())
host_name = socket.gethostname()

class ServerIO(PVGroup):
    ipaddress = pvproperty(value=ip_address, read_only = True, dtype = str, string_encoding='utf-8',report_as_string=True)
    hostname = pvproperty(value=host_name, read_only = True, dtype = str , string_encoding='utf-8',report_as_string=True)

    # NOTE the decorator used here:
    @ipaddress.startup
    async def ipaddress(self, instance, async_lib):
        # This method will be called when the server starts up.
        print('* request method called at server startup')
        self.io_get_queue = async_lib.ThreadsafeQueue()
        self.io_put_queue = async_lib.ThreadsafeQueue()


        # Loop and grab items from the response queue one at a time
        while True:
            value = await self.io_put_queue.async_get()
            print(f'Got put request from the device: {value}')
            if 'ipaddress' in list(value.keys()):
                await self.ipaddress.write(value['ipaddress'])



if __name__ == '__main__':
        ioc_options, run_options = ioc_arg_parser(
            default_prefix='NIH:PI1.',
            desc='Run an IOC that does blocking tasks on a worker thread.')

        ioc = ServerIO(**ioc_options)
        run(ioc.pvdb, **run_options)
