#!/usr/bin/env python3

class Client(object):
    def __init__(self):
        from caproto.threading.client import Context
        ctx = Context()
        dt,t,cpu,memory,battery = ctx.get_pvs('simple_daq:dt','simple_daq:TIME','simple_daq:CPU','simple_daq:MEMORY','simple_daq:BATTERY')

        self.dt,self.t,self.cpu,self.memory,self.battery  = dt,t,cpu,memory,battery

if __name__ == '__main__':
    client = Client()
