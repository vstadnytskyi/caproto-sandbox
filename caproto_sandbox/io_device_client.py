#!/usr/bin/env python3
from caproto.threading.client import Context
prefix='wt:'
ctx = Context()
request,response = ctx.get_pvs(prefix+'request',prefix+'response')
