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
def epics_client():
    print('epics Client')
    image = epics.PV(pvname = default_prefix+'image',connection_timeout = 20)
    t1 = time()
    img = image.get(timeout = 20)
    t2 = time()
    print(t2-t1, img.mean(), img.max(), img.min())
    img2 = img.reshape((3960,3960))
    print(t2-t1, img2.mean(), img2.max(), img2.min())

def caproto_client():
    print('caproto Client')
    ctx = Context()
    img_caproto, = ctx.get_pvs(default_prefix+'image')
    t1 = time()
    img_caproto_data = img_caproto.read()
    t2 = time()
    print(t2-t1, img_caproto_data.data.reshape((3960,3960)).mean(), img_caproto_data.data.reshape((3960,3960)).max(), img_caproto_data.data.reshape((3960,3960)).min())

epics_client()
caproto_client()
