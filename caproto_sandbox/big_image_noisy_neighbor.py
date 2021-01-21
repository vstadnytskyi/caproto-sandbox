#!/usr/bin/env python3

import time
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run
import numpy as np
from caproto import ChannelType

image_shape = (3960, 3960)


class IOInterruptIOC(PVGroup):
    t1 = pvproperty(value=2.0)
    image = pvproperty(
        value=np.random.randint(0, 255, image_shape, dtype = 'uint8').flatten(), dtype=int
    )

    @t1.startup
    async def t1(self, instance, async_lib):
        # Loop and grab items from the queue one at a time
        while True:
            await self.t1.write(time.monotonic())
            await self.image.write(np.random.randint(0, 255, image_shape, dtype = 'uint8').flatten())
            await async_lib.library.sleep(0.1)


if __name__ == "__main__":
    from tempfile import gettempdir
    print(f'temp-dir {gettempdir()}')

    from caproto import config_caproto_logging

    config_caproto_logging(file=gettempdir()+'/big_image_noisy_neibhor.log', level='DEBUG')

    ioc_options, run_options = ioc_arg_parser(
        default_prefix="big_image:",
        desc="Run an IOC that updates via I/O interrupt on key-press events.",
    )

    ioc = IOInterruptIOC(**ioc_options)
    print(ioc.image)
    run(ioc.pvdb, **run_options)
