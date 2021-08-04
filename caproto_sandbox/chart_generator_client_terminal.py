#!/usr/bin/python
# -*- coding: utf-8 -*-

from caproto.threading.client import Context
ctx = Context()

pvs = ctx.get_pvs('chart:image','chart:t1')


def read_pvs(pvs):
    for pv in pvs:
        print(pv.read().data)



if __name__ == '__main__':
    pass
