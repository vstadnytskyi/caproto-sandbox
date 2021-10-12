#!/usr/bin/env python3
from caproto.threading.client import Context
prefix='NIH:PI1.'
ctx = Context()
ipaddress, = ctx.get_pvs(prefix+'ipaddress')
hostname, = ctx.get_pvs(prefix+'hostname')

def data_to_str(arr):
    str = ''
    for i in arr:
        str += chr(i)
    return str

    
if __name__ == '__main__':
    pass
