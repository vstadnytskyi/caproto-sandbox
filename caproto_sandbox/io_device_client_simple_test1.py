#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from matplotlib import pyplot as plt
from logging import debug,warn,info,error
import epics
from time import time,sleep
from _thread import start_new_thread
from caproto.threading.client import Context
from pdb import pm
import epics
from numpy import nan, argmax

def get_image(N = 1):
    for i in range(N):
        arr = ca_img.read(timeout = 10).data

def plot(lst):
    from numpy import asarray
    from matplotlib import pyplot as plt
    plt.close('all')
    arr = asarray(lst)
    plt.plot(arr[:,0]-arr[0,0],arr[:,2]-arr[:,1])
    plt.plot(arr[:,0]-arr[0,0],arr[:,4]-arr[:,3])
    plt.xlabel('time')
    plt.ylabel('time difference')
    plt.title('time delay between variable accquired by device and published by IOC')

default_prefix='io_device_single:'
ctx = Context()
ca_img,ca_t1,ca_t2 = ctx.get_pvs(default_prefix+'image',default_prefix+'t1',default_prefix+'t2')
lst = []
def caproto_for_loop(N = 100):
    print('img,img.shape,img.max(),img.mean(),ca_t2.read().data[0]')
    for i in range(N):
        #img = ca_img.read().data
        t1 = ca_t1.read(data_type = 'time')
        t2 = ca_t2.read(data_type = 'time')
        t11 = t1.data[0]
        t12 = t1.metadata.timestamp
        t21 = t2.data[0]
        t22 = t2.metadata.timestamp
        lst.append([time(),t11,t12,t21,t22])
        sleep(1)
#pyepics_for_loop()
start_new_thread(caproto_for_loop,())
sleep(5)
get_image(3)
sleep(5)
get_image(3)
sleep(5)
get_image(3)
sleep(5)
get_image(3)
sleep(5)
plot(lst)
