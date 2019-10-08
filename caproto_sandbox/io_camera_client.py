#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
from logging import debug,warn,info,error
import epics
from time import time
from caproto.threading.client import Context
from pdb import pm
default_prefix='camera:'

print('epics Client')
image = epics.PV(pvname = default_prefix+'image', connection_timeout = 20)
t1 = time()
def image_get():
    """
    I have created this fucntion to simplify the call from timeit. 
    """
    global image
    return image.get(timeout = 20)
img = image.get(timeout = 20)
t2 = time()
print(t2-t1, img.mean(), img.max(), img.min())
img2 = img.reshape((3960,3960))

print('caproto Client')
ctx = Context()
img_caproto, = ctx.get_pvs(default_prefix+'image')
t1 = time()
img_caproto_data = img_caproto.read()
t2 = time()
print(t2-t1, img_caproto_data.data.reshape((3960,3960)).mean(), img_caproto_data.data.reshape((3960,3960)).max(), img_caproto_data.data.reshape((3960,3960)).min())


from timeit import timeit
t = timeit(image_get, number = 10)
print('pyepics client: {}'.format(t/10))
t = timeit(img_caproto.read, number = 10)
print('caproto client: {}'.format(t/10))
