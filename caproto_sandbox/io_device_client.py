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
img,t1,t2 = ctx.get_pvs(default_prefix+'image',default_prefix+'t1',default_prefix+'t2')
t1 = time()
img_data = img.read().data.reshape((3960,3960))
t2 = time()
