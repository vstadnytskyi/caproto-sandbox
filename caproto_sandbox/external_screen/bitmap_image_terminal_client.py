#!/usr/bin/env python3
"""
caproto server that generates a 8-bit bitmap image of given size
"""
from caproto.threading.client import Context
prefix='BITMAP_IMAGE:'
ctx = Context()
pv_name = prefix+'dt'
print(f'reading PV: {pv_name}')
dt, = ctx.get_pvs(pv_name)
pv_name = prefix+'image'
print(f'reading PV: {pv_name}')
image, = ctx.get_pvs(pv_name)