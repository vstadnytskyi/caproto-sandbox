#!/usr/bin/env python3
"""
simple data acquisisioin unit driver. This example collects reading from the onboard computer sensors.
"""


class Driver(object):
    def __init__(self):
        """
        initialization of the instance
        """
        from numpy import zeros
        self.arr = zeros((1,4))
        self.name = 'simple daq driver'

    def read(self):
        """
        reads onboard sensors and returns an array with a time-stamp.
        """
        import psutil
        from time import time
        import numpy as np
        memory = self.get_virtual_memory()
        cpu = self.get_CPU()
        battery = self.get_battery()
        arr = self.arr
        arr[0,0] = time()
        arr[0,1] = cpu
        arr[0,2] = memory
        arr[0,3] = battery
        return arr
    
    def get_CPU(self):
        import psutil
        import numpy as np
        cpu = psutil.cpu_percent()
        return cpu
    
    def get_virtual_memory(self):
        import psutil
        import numpy as np
        memory = psutil.virtual_memory().used
        return memory
    
    def get_battery(self):
        import psutil
        import numpy as np
        if psutil.sensors_battery() is not None:
            battery = psutil.sensors_battery().percent
        else:
            battery = np.nan
        return battery

if __name__ == '__main__':
    driver = Driver()
