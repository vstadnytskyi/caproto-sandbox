#!/usr/bin/env python3
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run
from textwrap import dedent


class SimpleIOC(PVGroup):
    """
    An IOC with three uncoupled read/writable PVs

    string PVs
    ----------
    str_in (string)
    str_out (string)

    """
    from numpy import random
    from time import time,sleep
    from pickle import dumps
    str_in = pvproperty(value='', dtype = str, max_length = 1000)
    str_in2 = pvproperty(value='', dtype = str, max_length = 1000)
    str_out = pvproperty(value='', dtype = str, read_only = True)
    N_chr = pvproperty(value=3, read_only = True)


    @str_in.startup
    async def str_in(self, instance, async_lib):
        'Periodically update the value'
        from time import time, sleep
        while True:
            await async_lib.library.sleep(1)

    @str_in.putter
    async def str_in(self, instance, value):
        print('str_in putter',value,type(value))
        await self.str_out.write(value=value.upper())
        await self.N_chr.write(value=len(value))

    @str_in2.putter
    async def str_in2(self, instance, value):
        print('str_in2 putter',value,type(value))
        await self.str_out.write(value=value.upper())
        await self.N_chr.write(value=len(value))

from ubcs_auxiliary.threading import start_new_safe_thread
if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='simple_str:',
        desc=dedent(SimpleIOC.__doc__))
    ioc = SimpleIOC(**ioc_options)
    run(ioc.pvdb, **run_options)
