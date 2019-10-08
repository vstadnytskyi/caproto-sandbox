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
default_prefix='io_device:'

image = epics.PV(pvname = default_prefix+'image')
t1 = epics.PV(pvname = default_prefix+'t1')
t2 = epics.PV(pvname = default_prefix+'t2')
lst = []
i_lst = [101,103,105,107,10,11,13,15,31,33,35,37,1,3,5,7]
def func(image,t1,t2):
    for i in range(240):
        img = run_once(image,t1,t2,i)
        if i == 10:
            plot(lst)
        if i == 30:
            plot(lst)
        if i == 100:
            plot(lst)
    plot(lst)

def run_once(image,t1,t2,i):
    img = None
    if i in i_lst:
        img = image.get(timeout = 20)
    if img is not None:
        lst.append([time(),t1.value,t1.timestamp,t2.value,t2.timestamp,img.mean()])
    sleep(1)
    return img
def get_img(image):
    img = image.get(timeout = 20)
    return img
#start_new_thread(func,(image,t1,t2))

def plot(lst):
    from matplotlib import pyplot as plt
    from numpy import asarray
    arr = asarray(lst)
    plt.figure()
    plt.plot(arr[:,0]-arr[0,0],arr[:,2]-arr[:,1],'ro')
    plt.plot(arr[:,0]-arr[0,0],arr[:,4]-arr[:,3],'go')
    plt.show()
func(image,t1,t2)
