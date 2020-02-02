#!/usr/bin/env python3
from caproto.threading.client import Context
prefix='simple_str:'
ctx = Context()
str_in, = ctx.get_pvs(prefix+'str_in')
str_in2, = ctx.get_pvs(prefix+'str_in2')
str_out, = ctx.get_pvs(prefix+'str_out')
N_chr, = ctx.get_pvs(prefix+'N_chr')

def array_to_chr(array):
    string = ''
    for i in range(len(array)):
        string += chr(array[i])
    return string

sub = str_out.subscribe()
responses = []
def f(response):
    responses.append(response)
token = sub.add_callback(f)
values = []
def g(response):
    values.append(response.data[0])
sub.add_callback(g)

print(str_in.write('this is test init string'))
print(str_out.read().data)
