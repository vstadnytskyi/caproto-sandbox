#!/usr/bin/env python3
"""
caproto server that generates a 8-bit bitmap image of given size
"""

from logging import debug,info,warning,error
#Input/Output server library
from caproto.server import pvproperty, PVGroup, SubGroup, ioc_arg_parser, run
#from ubcs_auxiliary.threading import new_thread
from numpy import nan, zeros, int16, random
width = 1920 #1920 #int(1920/2)
height = 1080 #1080#int(1080/2)

class Server(PVGroup):
    
    image = pvproperty(value=zeros((height,width,3)).flatten(), dtype = int, max_length = width*height*3*10)
    dt = pvproperty(value = 1)

    @image.startup #this fubction will be executed on instantiaton
    async def image(self, instance, async_lib):
        pos_w = 0
        pos_h = 0
        self.new_arr = zeros((height,width,3))
        while True:
            #new_arr = random.randint(256, size=(3, 1000, 500)).flatten()

            self.new_arr = self.new_arr*0
            #new_arr[int(height/2),:,1] = 255
            self.new_arr[:,pos_w,:] = 255
            self.new_arr[pos_h,:,:] = 255
            if pos_w == (width-1):
                pos_w = 0
            else:
                pos_w += 1
            if pos_h == (height-1):
                pos_h = 0
            else:
                pos_h += 1
            await self.image.write(value=self.new_arr.flatten())
            # Let the async library wait for the next iteration
            await async_lib.library.sleep(self.dt.value)
    #@image.putter
    #async def image(self, instance, value):

if __name__ == '__main__':
    # The Record Name is specified by prefix
    prefix = 'BITMAP_IMAGE:'
    from pdb import pm
    from tempfile import gettempdir
    import logging
    print(gettempdir()+'/{}.log'.format(prefix))
    logging.basicConfig(filename=gettempdir()+'/{}.log'.format(prefix),
                        level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    ioc_options, run_options = ioc_arg_parser(
        default_prefix=prefix,
        desc='description')

    io_server  = Server(**ioc_options)

    #start async caproto server IO
    run(io_server.pvdb, **run_options)