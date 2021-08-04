#!/usr/bin/env python3

import time
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run
import numpy as np
from caproto import ChannelType
import logging
image_shape = (240,640, 3)


class softIOC(PVGroup):
    arr = np.zeros(image_shape).flatten()
    t1 = pvproperty(value=1.0)
    image = pvproperty(value=arr, dtype = int, max_length = image_shape[0]*image_shape[1]*image_shape[2])

    x = [0]
    y1 = [np.nan]
    y2 = [np.nan]


    @t1.startup
    async def t1(self, instance, async_lib):
        # Loop and grab items from the queue one at a time
        while True:
            self.x.append(self.x[-1]+1)
            self.y1.append(np.random.randint(255))
            self.y2.append(np.random.randint(255))
            await self.t1.write(time.monotonic())
            img = self.chart(np.asarray(self.x),np.asarray(self.y1),np.asarray(self.y2)).flatten()
            await self.image.write(value = img)
            await async_lib.library.sleep(.1)

    def chart(self, x,y1, y2):
        """
        charting function that takes x and y
        """
        xs_font = 10
        s_font = 12
        m_font = 16
        l_font = 24
        xl_font = 32

        import io
        from matplotlib.figure import Figure
        from matplotlib import pyplot
        from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
        from scipy import stats
        figure = Figure(figsize=(8,3),dpi=80)#figsize=(7,5))
        axes1 = figure.add_subplot(2,1,1)

        axes1.plot(x,y1, color = 'red', marker = 'o', markersize = 3 )

        axes1.set_title("Top subplot")
        axes1.set_xlabel("x (value)")
        axes1.set_ylabel("y (value)")
        axes1.tick_params(axis='y', which='both', labelleft=True, labelright=False, labelsize = m_font)
        axes1.grid(True)

        axes2 = figure.add_subplot(2,1,2)

        axes2.plot(x,y2, color = 'red', marker = 'o', markersize = 3 )

        axes2.set_title("Bottom subplot")
        axes2.set_xlabel("x (value)")
        axes2.set_ylabel("y (value)")
        axes2.tick_params(axis='y', which='both', labelleft=True, labelright=False, labelsize = m_font)
        axes2.grid(True)

        figure.tight_layout()
        figure_buf = io.BytesIO()
        figure.savefig(figure_buf, format='jpg')
        figure_buf.seek(0)
        import PIL
        image = np.asarray(PIL.Image.open(figure_buf))
        return image


if __name__ == "__main__":
    from tempfile import gettempdir
    print(f'temp-dir {gettempdir()}')

    from caproto import config_caproto_logging

    config_caproto_logging(file=gettempdir()+'/chart_generator.log', level='DEBUG')

    ioc_options, run_options = ioc_arg_parser(
        default_prefix="chart:",
        desc="SoftIOC generates a matplotlib plot of some data.",
    )


    ioc = softIOC(**ioc_options)
    print(ioc.image)
    run(ioc.pvdb, **run_options)
