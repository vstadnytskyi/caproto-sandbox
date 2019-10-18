#!/usr/bin/env python3
from caproto.threading.client import Context
prefix='simple_str:'
ctx = Context()
str_in, = ctx.get_pvs(prefix+'str_in')
str_out, = ctx.get_pvs(prefix+'str_out')
N_chr, = ctx.get_pvs(prefix+'N_chr')

def array_to_chr(array):
    string = ''
    for i in range(len(array)):
        string += chr(array[i])
    return string
