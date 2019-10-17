#!/usr/bin/env python3
import psutil
from time import sleep
sleep(2)
print(psutil.cpu_percent(percpu = True),'start')

from caproto.threading.client import Context
sleep(2)
print(psutil.cpu_percent(percpu = True), 'import Context')

ctx = Context()
sleep(2)
print(psutil.cpu_percent(percpu = True),'2 seconds after ctx = Context()')
sleep(2)
print(psutil.cpu_percent(percpu = True),'4 seconds after ctx = Context()')
sleep(2)
print(psutil.cpu_percent(percpu = True),'6 seconds after ctx = Context()')
