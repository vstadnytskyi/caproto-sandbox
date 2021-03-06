#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Beamline Configuration Server. Primarly used to service the Beamline configuration panel and provide flexibility in communication with 14IDB motors.

#Configuration Modes
#!/usr/bin/env python3

from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run
from caproto import ChannelType
from logging import debug, info, warning, error

from time import sleep
from tempfile import gettempdir
import os
from ubcs_auxiliary.saved_property import DataBase, SavedProperty

def move_motor(pos,put_queue):
    from numpy import arange
    from time import sleep
    print("move_motor")
    step = 0.001
    steps_per_second = 1000
    update = 0.5
    curr = float(io.RBV.value)
    if curr > pos:
        step = - step
    arr = list(arange(curr,pos,step*steps_per_second*update))
    lst = list(arr) + [pos]
    print(lst)
    for item in lst:
        print(item)
        put_queue.put({'pv':'RBV','value':item})
        sleep(update)



class Server(PVGroup):

    RBV = pvproperty(value=0.0,
                    read_only = True,
                    upper_alarm_limit=6.0,
                    lower_alarm_limit=-1.0,
                    upper_warning_limit=5.5,
                    lower_warning_limit=-1.0,
                    units="mm",
                    precision=3,
                    doc='motor position')
    VAL = pvproperty(value=0.0,
                    upper_alarm_limit=6.0,
                    lower_alarm_limit=-1.0,
                    upper_warning_limit=5.5,
                    lower_warning_limit=-1.0,
                    upper_ctrl_limit=7.0,
                    lower_ctrl_limit=-3.0,
                    units="mm",
                    precision=3,
                    doc='motor position')

    running = pvproperty(value=1)

    @running.startup
    async def running(self, instance, async_lib):
        """
        the running function will be executed on creation and startup of the running PV.

        first, it creates two asynchronous threadsafe queues: put_queue and get_queue.
        Second it start "while True" loop which checks if there are any entries in the put_queue. This is a pathway to communicate between outside objects.
        """
        print('* request method called at server startup @start.startup')
        self.put_queue = async_lib.ThreadsafeQueue()
        self.get_queue = async_lib.ThreadsafeQueue()
        while True:
            if True: #self.put_queue is not None:
                entry = await self.put_queue.async_get()
                print(f'Async Put Queue: Got put request from the device: {entry}')
                pv = entry['pv']
                value = entry['value']
                if pv == 'RBV':
                    await self.RBV.write(value)
            else:
                await async_lib.library.sleep(0.1)

    @RBV.getter
    async def RBV(self, instance):
        """
        this function is called when the RBV is read by a client
        """
        print('RBV getter:',self.RBV.value)

    @RBV.putter
    async def RBV(self, instance, value):
        print('RBV putter:',value)

    @VAL.putter
    async def VAL(self, instance, value):
        print('VAL getter',value)
        from _thread import start_new_thread
        start_new_thread(move_motor,(float(value),self.put_queue))
        #await self.put_queue.async_put({'pv':'RBV','value':value})

if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='BEAMLINE:motor.',
        desc='description')
    io  = Server(**ioc_options)

    #start async caproto server IO
    run(io.pvdb, **run_options)
