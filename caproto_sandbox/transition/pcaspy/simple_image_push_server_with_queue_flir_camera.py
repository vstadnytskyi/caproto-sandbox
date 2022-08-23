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

from pcaspy import SimpleServer as CAServer, Driver as Server
import random
from numpy import nan, zeros, int16, random
WIDTH = 2736
HEIGHT = 2192
print(f'width = {WIDTH}, height = {HEIGHT}')
prefix = 'BITMAP_IMAGE:'
pvdb = {
    'image' : {
        'prec' : 1,
        'count': WIDTH*HEIGHT*3,
    },
    'dt' : {
        'value': 1.0,
        'prec' : 1,
        'scan' : .1,
        'count': 1,
        'unit': 's' 
    },
}


class MyServer(Server):
    def __init__(self):
        super(MyServer, self).__init__()
        self.io_push_queue = None
        self.width = WIDTH
        self.height = HEIGHT
        from time import time
        self.t_start = time()
        import threading
        threading.Thread(target=self.poll, daemon=True).start()

    def poll(self):
        while True:
            if self.io_push_queue is not None:
                entry = self.io_push_queue.get(block=True)
                for key, value in entry.items():
                    self.setParam(key, value)
            self.updatePVs()


    def read(self, reason):
        from time import ctime, time
        import psutil
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
    import queue
    from time import sleep,ctime, time

    config_filename = r'C:\Users\AR-VR lab W1\Documents\Valentyn\custom_python_libraries\instrumentation\flir-camera\config_SN14120164_12bit.conf'
    from lcp_flir.flir_camera_DL import FlirCamera
    from lcp_flir.device_level_server import Server
    camera = FlirCamera()
    camera.init(config_filename)
    device = camera
    caserver = CAServer()
    caserver.createPV(prefix, pvdb)
    myserver = MyServer()
    io_push_queue = queue.Queue()
    myserver.io_push_queue = io_push_queue
    device.io_push_queue = io_push_queue
    import numpy as np
    from ubcs_auxiliary.multithreading import new_thread
    caserver.dt = 1
    def func():
        from time import time, sleep, ctime
        import cv2
        import numpy as np
        from logging import debug, info, warning, error
        t1 = time()
        device.broadcasting = True
        caserver.flag = True
        i = 0
        img = myserver.read("image")
        img_reshaped = np.asarray(img).reshape((2192, 2736, 3))
        while device.broadcasting:
            t_start = time()
            if not camera.queue.isempty:
                t1 = time()
                image = camera.convert_raw_to_image(camera.queue.dequeue(N=1)[0])
                t2 = time()
                debug('1',t2-t1,camera.queue.length)
                t1 = time()
                if caserver.flag:
                    out = image
                    out = cv2.normalize(image, out, 0, 255, cv2.NORM_MINMAX)
                    img_reshaped[:, :, 1] = out.astype("float64")
                else:
                    img_reshaped[:, :, 1] = image
                t2 = time()
                debug('2',t2-t1,camera.queue.length)
                t1 = time()
                dc = {}
                dc['image'] = img_reshaped.flatten()
                dc['dt'] = i
                io_push_queue.put(dc)
                t2 = time()
                debug('3',t2-t1,camera.queue.length)
                i+=1
                t2 = time()
                debug('f',t2-t_start,camera.queue.length)
            else:
                sleep(0.1)

    new_thread(func,)

    caserver.processing = True
    def gunc():
        while caserver.processing:
            caserver.process(0.1)


    new_thread(gunc,)
            