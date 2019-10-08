#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from logging import debug,warn,info,error
import epics
from time import time
from caproto.threading.client import Context
from pdb import pm
default_prefix='io_device:'

ctx = Context()
img_caproto, = ctx.get_pvs(default_prefix+'image')


t1 = epics.PV(pvname = default_prefix+'t1' )
dt1 = epics.PV(pvname = default_prefix+'dt1' )
t2 = epics.PV(pvname = default_prefix+'t2' )
dt2 = epics.PV(pvname = default_prefix+'dt2' )
image = epics.PV(pvname = default_prefix+'image',connection_timeout = 20)
t1 = time()
img = image.get(timeout = 20)
t2 = time()
print(t2-t1, img.mean(), img.max(), img.min())
img2 = img.reshape((3960,3960))
print(t2-t1, img2.mean(), img2.max(), img2.min())


t1 = time()
img_caproto_data = img_caproto.read().data.reshape((3960,3960))
t2 = time()
print(t2-t1, img_caproto_data.mean(), img_caproto_data.max(), img_caproto_data.min())
