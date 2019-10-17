#!/usr/bin/env python3
import psutil
from time import sleep
sleep(2)
print(psutil.cpu_percent(percpu = True))

from caproto.threading.client import Context
sleep(2)
print(psutil.cpu_percent(percpu = True))

ctx = Context()
sleep(2)
print(psutil.cpu_percent(percpu = True))
sleep(2)
print(psutil.cpu_percent(percpu = True))
sleep(2)
print(psutil.cpu_percent(percpu = True))
