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

prefix = 'simple_daq:'
pvdb = {
    'CPU' : {
        'value': 0.0,
        'prec' : 1,
        'scan' : 1,
        'count': 1,
        'unit': '%'
    },
    'MEMORY' : {
        'value': 0.0,
        'prec' : 1,
        'scan' : 1,
        'count': 1,
        'unit': 'GB'
    },
    'BATTERY' : {
        'value': 0.0,
        'prec' : 1,
        'scan' : 1,
        'count': 1,
        'unit': '%'
       },
    'TIME' : {
        'type' : 'str',
        'value': 'time',
        'scan' : 1,
            },
    'dt' : {
        'value': 0.0,
        'prec' : 1,
        'scan' : 1,
        'count': 1,
        'unit': 's' 
    },
}


class myDriver(Driver):
    def __init__(self):
        super(myDriver, self).__init__()

    def read(self, reason):
        from time import ctime, time
        import psutil
        if reason == 'TIME':
            value = ctime(time())
        elif reason == 'CPU':
            value = psutil.cpu_percent()
        elif reason == 'BATTERY':
            if psutil.sensors_battery() is not None:
                value = psutil.sensors_battery().percent
            else:
                value = np.nan
        elif reason == 'MEMORY':
            value = psutil.virtual_memory().used / (1024**3)
        else:
            value = self.getParam(reason)
        return value

if __name__ == '__main__':
    from time import sleep,ctime, time
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()
    while True:
        server.process(driver.getParam('dt'))
        print(ctime(time()))