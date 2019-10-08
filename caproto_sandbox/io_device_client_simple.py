#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from logging import debug,warn,info,error
import epics
from time import time,sleep
from _thread import start_new_thread
from caproto.threading.client import Context
from pdb import pm
import epics
from numpy import nan
default_prefix='io_device_single:'
ctx = Context()
ca_img,ca_t1,ca_t2 = ctx.get_pvs(default_prefix+'image',default_prefix+'t1',default_prefix+'t2')


image = epics.PV(pvname = default_prefix+'image', connection_timeout = 20)
t1 = epics.PV(pvname = default_prefix+'t1')
t2 = epics.PV(pvname = default_prefix+'t2')


def pyepics_for_loop():
    print('img,img.shape,img.max(),img.mean(),t1.get(),t2.get()')
    for i in range(4):
        img = image.get(timeout = 20)
        print(img,img.shape,img.max(),img.mean(),t1.get(),t2.get())
        sleep(1)

def caproto_for_loop():
    print('img,img.shape,img.max(),img.mean(),ca_t2.read().data[0]')
    for i in range(4):
        img = ca_img.read().data
        print(img,img.shape,img.max(),img.mean(),ca_t2.read().data[0])
        sleep(1)
