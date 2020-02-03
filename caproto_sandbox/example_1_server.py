#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#Beamline Configuration Server. Primarly used to service the Beamline configuration panel and provide flexibility in communication with 14IDB motors.

from EPICS_CA.CAServer import casput
#Configuration Modes
#!/usr/bin/env python3

from caproto.server import pvproperty, PVGroup, SubGroup, ioc_arg_parser, run
from caproto import ChannelType
from logging import debug, info, warning, error

from time import sleep
from tempfile import gettempdir
import os
from ubcs_auxiliary.saved_property import DataBase, SavedProperty

class Choices():

    db = DataBase(root = os.getcwd(), name = 'Choices')
    saved_positions = SavedProperty(db,'saved_positions',{}).init()
    tweak_pos_value = SavedProperty(db,'tweak_value',0.001).init()

    def __init__(self):
        from caproto.threading.client import Context
        ctx = Context()
        self.monitor, = ctx.get_pvs('BEAMLINE:motor.VAL')
        self.sub = self.monitor.subscribe()
        self.token = self.sub.add_callback(self.callback_monitor)

        self.insert_pos = 0.0
        self.retract_pos = 5.0


    def callback_monitor(self,sub, response = None):
        """
        monitor callback functnio will be executed when a PV is written into.
        """
        print('callback_monitor: Received response from', sub.data[0])
        if abs(sub.data[0] - self.insert_pos) < 0.002:
            dict = {}
            dict['pv'] = 'choices'
            dict['value'] = "Insert"
        elif abs(sub.data[0] - self.retract_pos) < 0.002:
            dict = {}
            dict['pv'] = 'choices'
            dict['value'] = "Retract"
        else:
            dict = {}
            dict['pv'] = 'choices'
            dict['value'] = " "
        io.put_queue.put(dict)

    def get_state(self):
        curr = self.monitor.read().data[0]
        print(f'get_state {curr} and insert {self.insert_pos} and retract {self.retract_pos}')
        print(f'{abs(curr - self.insert_pos) < 0.002}')
        if abs(curr - self.insert_pos) < 0.002:
            reply = "Insert"
        elif abs(curr - self.retract_pos) < 0.002:
            reply = "Retract"
        else:
            reply = " "
        print(f'get_state {reply}')
        return {'pv':'choices','value':reply}

    def insert(self):
        self.monitor.write(self.insert_pos)
    def retract(self):
        self.monitor.write(self.retract_pos)

    def insert_filter(self, name = None):
        pass

class Motors():
    """Motor client object. Connects to selected PVs"""

    db = DataBase(root = os.getcwd(), name = 'Motor')
    tweak_pos_value = SavedProperty(db,'tweak_pos_value',0.050).init()

    def __init__(self):
        from caproto.threading.client import Context
        ctx = Context()
        self.rbv_monitor, self.val_monitor = ctx.get_pvs('BEAMLINE:motor.RBV', 'BEAMLINE:motor.VAL')

        #create subscription objects
        self.sub = {}
        self.sub['rbv_monitor'] = self.rbv_monitor.subscribe()
        self.sub['val_monitor'] = self.val_monitor.subscribe()

        #bind callback function with the subscription objects. The bound callback function will be called if new PV is posted.
        self.token = {}
        self.token['rbv_monitor'] = self.sub['rbv_monitor'].add_callback(self.rbv_monitor_callback)
        self.token['val_monitor'] = self.sub['val_monitor'].add_callback(self.val_monitor_callback)


    def rbv_monitor_callback(self,sub, response = None):
        print('rbv_monitor_callback: Received response from', sub.data[0])
    def val_monitor_callback(self,sub, response = None):
        print('val_monitor_callback: Received response from', sub.data[0])

    def jog(self, value = 0.5):
        from time import sleep
        print('Server to Motor: move positive')
        curr = self.val_monitor.read().data[0]
        new = curr + value
        self.val_monitor.write(float(new))
        sleep(2.5)
        print('Server to Motor: move negative')
        curr = self.val_monitor.read().data[0]
        new = curr - value
        self.val_monitor.write(float(new))

    def tweak_pos_up(self,):
        print('Motor: tweak_pos_up')
        curr = self.val_monitor.read().data[0]
        new = curr + self.tweak_pos_value
        self.val_monitor.write(new)

    def tweak_pos_down(self):
        print('Motor: tweak_pos_down')
        curr = self.y_val_monitor.read().data[0]
        new = curr - self.tweak_pos_value
        self.y_val_monitor.write(new)

class Server(PVGroup):
    io_put_queue = None

    # DOWNSTREAM TABLE
    running = pvproperty(value=1)
    jog = pvproperty(value=0.0)
    enum_strings=['Insert','Retract',' ']
    choices = pvproperty(value=' ',enum_strings=enum_strings , dtype=ChannelType.ENUM)

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
                if pv == 'jog':
                    await self.jog.write(value)
                if pv == 'choices':
                    await self.choices.write(value)
            else:
                await async_lib.library.sleep(0.1)

    @jog.putter
    async def jog(self, instance, value):
        """
        called when the a new value is written into "jog" PV
        """
        print(f"Server: {'jog'} Got 'put' request from outside: new value is {value} and type {type(value)}")
        if float(value) == 1.0:
            motors.jog()
            print('jogging motor')
        print(f"{self.jog.value},{float(value)}")
        if self.jog.value == 0.0 and float(value) == 1.0:
            await self.put_queue.async_put({'pv':'jog','value':0.0})

    @jog.getter
    async def jog(self, instance):
        """
        called when the a new value is readby a client
        """
        pass

    @choices.putter
    async def choices(self, instance, value):
        print(f"PV: {'choices.putter'} new value is {value} and current {self.choices.value}")
        curr = self.choices.value
        if value == 'Retract' and curr != 'Retract':
            choices.retract()
        elif value == "Insert" and curr != 'Insert':
            choices.insert()
        else:
            pass
        import asyncio
        await asyncio.sleep(0.1)


    @choices.startup
    async def choices(self, instance, value):
        print(f"PV: {'choices.startup'} current state is {choices.get_state()}")
        await self.put_queue.async_put(choices.get_state())

if __name__ == '__main__':
    choices = Choices()
    motors = Motors()



    ioc_options, run_options = ioc_arg_parser(
        default_prefix='BEAMLINE:SERVER.',
        desc='description')
    io  = Server(**ioc_options)

    #start async caproto server IO
    run(io.pvdb, **run_options)
