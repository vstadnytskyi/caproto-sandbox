#!/usr/bin/env python3
import termios
import fcntl
import sys
import os
import threading
import atexit
from time import time,sleep
from datetime import datetime

from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run
from numpy import zeros, random
image_shape = (3960,3960)
class Device(object):
    dt = 1
    def start_io_interrupt_monitor(self,new_value_callback):
        '''
        This function monitors the terminal it was run in for keystrokes.
        On each keystroke, it calls new_value_callback with the given keystroke.

        This is used to simulate the concept of an I/O Interrupt-style signal from
        the EPICS world. Those signals depend on hardware to tell EPICS when new
        values are available to be read by way of interrupts - whereas we use
        callbacks here.
        '''
        while True:
            image = random.randint(0,256,image_shape).flatten()
            new_value_callback({'image':image})
            print('image in device:',image.mean(),image.max(),image.min())
            sleep(self.dt)


class IOInterruptIOC(PVGroup):
    arr = zeros(image_shape)
    f_arr = arr.flatten()
    image = pvproperty(value = f_arr, dtype = float)

    @image.startup
    async def image(self, instance, async_lib):
        # This method will be called when the server starts up.
        print('* t1 method called at server startup')
        queue = async_lib.ThreadsafeQueue()

        # Start a separate thread that monitors keyboard input, telling it to
        # put new values into our async-friendly queue
        thread = threading.Thread(target=device.start_io_interrupt_monitor,
                                  daemon=True,
                                  kwargs=dict(new_value_callback=queue.put))
        thread.start()

        # Loop and grab items from the queue one at a time
        while True:
            value = await queue.async_get()
            if 'image' in list(value.keys()):
                await self.image.write(value['image'])
                print('image in ioc:',self.image.value.mean(),self.image.value.max(),self.image.value.min())

device = Device()

if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='camera:',
        desc='Run an IOC that updates via I/O interrupt on key-press events.')

    ioc = IOInterruptIOC(**ioc_options)
    print(ioc.image)
    run(ioc.pvdb, **run_options)
