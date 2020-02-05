#!/usr/bin/env python3
import itertools
import threading
import time

from caproto.server import pvproperty, PVGroup, ioc_arg_parser, run

class Server(PVGroup):
    request = pvproperty(value=0.0)
    response = pvproperty(value=123456789012345.0)

    # NOTE the decorator used here:
    @request.startup
    async def request(self, instance, async_lib):
        # This method will be called when the server starts up.
        print('* request method called at server startup')
        self.request_queue = async_lib.ThreadsafeQueue()
        self.response_queue = async_lib.ThreadsafeQueue()

        # Start a separate thread that consumes requests and sends responses.
        thread = threading.Thread(target=device.get_time,
                                  daemon=True,
                                  kwargs=dict(request_queue=self.request_queue,
                                              response_queue=self.response_queue))
        thread.start()

        # Loop and grab items from the response queue one at a time
        while True:
            value = await self.response_queue.async_get()
            print(f'Got a response from the worker: {value}')

            # Propagate the keypress to the EPICS PV, triggering any monitors
            # along the way
            await self.response.write(value)

    @request.putter
    async def request(self, instance, value):
        print(f'Sending the request {value} to the worker.')
        await self.request_queue.async_put(value)
        return value


if __name__ == '__main__':
    ioc_options, run_options = ioc_arg_parser(
        default_prefix='wt:',
        desc='Run an IOC that does blocking tasks on a worker thread.')

    from worker_thread_device import Device
    device = Device()

    ioc = Server(**ioc_options)
    run(ioc.pvdb, **run_options)
