#!/usr/bin/env python3
import itertools
import threading
import time

from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run

class Device():
    def get_time(self, request_queue, response_queue):
        """
        In this toy example, the "request" is some number of seconds to sleep for, but it could be any blocking task. For example, it can be a command to a device to perform some task.

        In this example, we return current time after sleeping 0.2 s. This emulates communication to a device that takes time and return of the new value.
        """

        from time import sleep, time

        print(f'performing the task of reading "position"')
        sleep(0.2)
        position = time()
        # In this toy example, the "response" is just a counter of how many
        # requests we have seen, but it could be anything.
        response_queue.put(position)


if __name__ == '__main__':
    pass
