#!/usr/bin/env python
"""
    CPU = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = '%')

    MEMORY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = 'GB')

    BATTERY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = '%')

    TIME = pvproperty(value='time unknown', read_only = True, dtype = str)

    dt = pvproperty(value=1.0, precision = 3, units = 's')


"""

from pcaspy import SimpleServer, Driver
import random
from numpy import nan, zeros, int16, random
width = 15 #1920 #int(1920/2)
height = 15 #1080#int(1080/2)

prefix = 'BITMAP_IMAGE:'
pvdb = {
    'image' : {
        'prec' : 1,
        'count': width*height*3,
    },
    'dt' : {
        'value': 1.0,
        'prec' : 1,
        'scan' : .1,
        'count': 1,
        'unit': 's' 
    },
}


class myDriver(Driver):
    def __init__(self):
        super(myDriver, self).__init__()
        self.width = width
        self.height = height
        from time import time
        self.t_start = time()
        import threading
        threading.Thread(target=self.poll, daemon=True).start()

    def poll(self):
        from time import ctime, time, sleep
        import psutil
        width = self.width
        height = self.height
        pos_w = 0
        pos_h = 0
        self.new_arr = zeros((height,width,3), dtype='int16')
        while True:

            self.new_arr = self.new_arr*0
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
            self.setParam('image', self.new_arr.flatten())
            self.updatePVs()

            sleep(self.getParam('dt'))

    # def read(self, reason):
    #     from time import ctime, time
    #     import psutil
    #     if reason == 'TIME':
    #         value = time()-self.t_start
    #     elif reason == 'CPU':
    #         value = psutil.cpu_percent()
    #     elif reason == 'BATTERY':
    #         if psutil.sensors_battery() is not None:
    #             value = psutil.sensors_battery().percent
    #         else:
    #             value = np.nan
    #     elif reason == 'MEMORY':
    #         value = psutil.virtual_memory().used / (1024**3)
    #     else:
    #         value = self.getParam(reason)
    #     return value

    def write(self, reason, value):
        from time import ctime, time
        import psutil
        if reason == 'dt':
            print(f"dt was written and new dt is {value}")
            self.setParam(reason,value)

if __name__ == '__main__':
    from time import sleep,ctime, time
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()
    while True:
        server.process(0.1)