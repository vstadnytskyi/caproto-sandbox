#!/usr/bin/env python3

import time
from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run
import numpy as np
from caproto import ChannelType

image_shape = (768, 216)


class Server(PVGroup):
    t1 = pvproperty(value=2.0)
    shape = pvproperty(value=image_shape)
    image = pvproperty(
        value=np.random.randint(0, 255, image_shape, dtype = 'uint8').flatten(), dtype=bytes, max_length = 470448000
    )
    x = []
    y = []

    @t1.startup
    async def t1(self, instance, async_lib):
        # Loop and grab items from the queue one at a time
        while True:
            await self.t1.write(time.monotonic())
            self.x.append(self.t1.value)
            self.y.append(np.random.randint(0,256))
            image_shape = self.shape.value
            arr = self.figure_to_array(self.chart_one(x=self.x,y=self.y,shape = image_shape)).flatten()
            await self.image.write(arr)

            await async_lib.library.sleep(1)

    @shape.putter
    async def shape(self, instance, value):
        print('shape putter:',value)


    def chart_one(self,x,y, shape, dpi = 100):
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
        figure = Figure(figsize=(shape[0]/dpi,shape[1]/dpi),dpi=dpi)#figsize=(7,5))
        axes = figure.add_subplot(1,1,1)
        from numpy import nonzero, zeros,nan, ones, argwhere, mean, nanmean, arange
        from scipy import stats


        axes.plot(x,y,'-o',color = 'lightblue')

        axes.set_title("Last Depressurize Event",fontsize=m_font, color = 'g')
        axes.set_xlabel("Time (ms)",fontsize=m_font)
        axes.set_ylabel("Pressure",fontsize=m_font)
        axes.tick_params(axis='y', which='both', labelleft=True, labelright=False, labelsize = m_font)

        axes.grid(True)
        axes.set_facecolor('xkcd:salmon')

        figure.tight_layout()
        return figure

    def figure_to_array(self, figure):
        from io import BytesIO
        from PIL.Image import open
        from numpy import asarray
        figure_buf = BytesIO()
        figure.savefig(figure_buf, format='jpg')
        figure_buf.seek(0)
        image = asarray(open(figure_buf))
        return image

if __name__ == "__main__":
    from tempfile import gettempdir
    print(f'temp-dir {gettempdir()}')

    from caproto import config_caproto_logging

    config_caproto_logging(file=gettempdir()+'/big_image_noisy_neibhor.log', level='DEBUG')

    ioc_options, run_options = ioc_arg_parser(
        default_prefix="bitmap_generator:",
        desc="Run an IOC that updates via I/O interrupt on key-press events.",
    )

    ioc = Server(**ioc_options)
    print(ioc.image)
    run(ioc.pvdb, **run_options)
