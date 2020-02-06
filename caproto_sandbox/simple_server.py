#!/usr/bin/env python3
from caproto.server import pvproperty, PVGroup

class SimpleIOC(PVGroup):
    """
    An IOC with three uncoupled PVs

    Scalar PVs
    ----------
    running (int)
    rbv (int)
    val (int)

    """
    running = pvproperty(value=0)
    rbv = pvproperty(value=0)
    val = pvproperty(value=0)

    @running.startup
    async def running(self, instance, async_lib):
        'Periodically update the value'
        self.running.write(1)
        self.put_queue = async_lib.ThreadsafeQueue()
        self.get_queue = async_lib.ThreadsafeQueue()
        while True:
            entry = await self.put_queue.async_get()
            pv = entry['pv']
            value = entry['value']
            if pv == 'rbv':
                print("process a 'rbv' put request from a device")
            if pv == 'val':
                print("process a 'val' put request from a device")

    @val.putter
    async def val(self, instance, value):
        """
        called when the a new value is written into "val" PV
        """
        print(f"Server: 'rbv' Got 'put' request from outside: new value is {value} and type {type(value)}")
        print('responding to the put request...')

    @val.getter
    async def val(self, instance):
        """
        called when the a new value is readby a client
        """
        print(f"Server: 'rbv' Got 'get' request from outside:"")
        print('responding to the get request...')

if __name__ == '__main__':
    from caproto.server import ioc_arg_parser, run
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='simple:',
        desc=dedent(SimpleIOC.__doc__))
    ioc = SimpleIOC(**ioc_options)
    run(ioc.pvdb, **run_options)
