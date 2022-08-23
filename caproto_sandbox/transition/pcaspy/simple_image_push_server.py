#!/usr/bin/env python
"""
    CPU = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = '%')

    MEMORY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = 'GB')

    BATTERY = pvproperty(value=0.0, read_only = True, dtype = float, precision = 1, units = '%')

    TIME = pvproperty(value='time unknown', read_only = True, dtype = str)

    dt = pvproperty(value=1.0, precision = 3, units = 's')


"""
import os
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = str(4000*4000*3*10)

from pcaspy import SimpleServer, Driver
import random
from numpy import nan, zeros, int16, random
WIDTH = 2736
HEIGHT = 2192
print(f'width = {WIDTH}, height = {HEIGHT}')
print('simple push server')
prefix = 'BITMAP_IMAGE:'
pvdb = {
    'image' : {
        'prec' : 0,
        'count': WIDTH*HEIGHT*3,
    },
    'dt' : {
        'value': 1.0,
        'prec' : 1,
        'count': 1,
        'unit': 's' 
    },
}


class myDriver(Driver):
    def __init__(self):
        super(myDriver, self).__init__()
        self.width = WIDTH
        self.height = HEIGHT
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
        self.new_arr = zeros((height,width,3), dtype='uint8')

    def read(self, reason):
        from time import ctime, time
        import psutil
        print('read',reason, time())
        if reason == 'image': 
            value = self.getParam('image')
        elif reason == 'dt':
            value = self.getParam('dt')
        
        return value

    def write(self, reason, value):
        from time import ctime, time
        import psutil
        import numpy as np
        if reason == 'dt':
            self.setParam(reason,value)
        elif reason == 'image':
            self.setParam(reason,value)

if __name__ == '__main__':
    from time import sleep,ctime, time
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()
    while True:
        server.process(.1)