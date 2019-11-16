#!/usr/bin/env python3
"""
Authors: Valentyn Stadnytskyi
Date created: 23 Oct 2019
Date last modified: 25 Oct 2019
Python Version: 3

Description:
------------
The Syringe Pump Tower Input-Output module
"""

from logging import debug,info,warning,error
#Input/Output server library
from caproto.server import pvproperty, PVGroup, SubGroup, ioc_arg_parser, run
#from ubcs_auxiliary.threading import new_thread
from numpy import nan, zeros, int16, random



class Server(PVGroup):
    arr = zeros((3,100,100)).flatten()
    image = pvproperty(value=arr, dtype = int, max_length = 400000)
    image_mean = pvproperty(value=0.0, precision = 3)

    @image.startup #this fubction will be executed on instantiaton
    async def image(self, instance, async_lib):
        while True:
            new_arr = random.randint(256, size=(3, 100, 100)).flatten()
            await self.image.write(value=new_arr)
            await self.image_mean.write(value=new_arr.mean())
            # Let the async library wait for the next iteration
            await async_lib.library.sleep(1)

if __name__ == '__main__':
    # The Record Name is specified by prefix
    prefix = 'TEST.'
    from pdb import pm
    from tempfile import gettempdir
    import logging
    print(gettempdir()+'/{}.log'.format(prefix))
    logging.basicConfig(filename=gettempdir()+'/{}.log'.format(prefix),
                        level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s")

    ioc_options, run_options = ioc_arg_parser(
        default_prefix=prefix,
        desc='description')

    io_server  = Server(**ioc_options)

    #start async caproto server IO
    run(io_server.pvdb, **run_options)
