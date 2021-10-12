=====================================
Example Simple Data Acquisition Unit
=====================================

This is an example of a simple data acquisition unit. The data comes from onboard sensors like: CPU utilization, battery capacity and memory utilization.

The example is purposely divided into several different files to explicitly show the modularity of this example. The files are: driver, device, server, gui, and client.

The *driver* file contains one Driver class. The instantiation of the class connects to a data acquisition unit and provides a simple read() function to read from sensors. The result is returned as a numpy array, in this case 1x4 with entries sorted as following: time, CPU utilization in %, memory utilization in GB, battery capacity in %.

The next level in the hierarchy is device level. The device code consists of one Device class. The initialization of the device instance creates circular buffer where the data from the data acquisition unit will be stored. This example does not take advantage of the circular buffer explicitly, but it can be used to expand the example in future and add more fields like mean CPU usage, etc.

The server code puts entire example on the network using caproto library. The server level has six Process Variables(PVs):  TIME, CPU, MEMORY, BATTERY, dt, LIST
- TIME - time of last read (UnixTime)
- CPU - CPU utilization value during last read
- MEMORY - MEMORY utilization value during last read
- BATTERY - BATTERY utilization value during last read
- dt - update frequency in seconds
- LIST - combined PV that transmits all data acquired during last data acquisition


.. code-block:: shell

    run worker_thread_server.py

You should see something similar to the following 5 lines:

.. code-block:: shell

  $ ipython3 caproto_sandbox/worker_thread_server.py
  [I 18:20:17.919          server:  162] Asyncio server starting up...
  [I 18:20:17.920          server:  175] Listening on 0.0.0.0:57804
  [I 18:20:17.920          server:  261] Server startup complete.
  * request method called at server startup

Now with the client you can submit a command to a "request" PV and check response in the "response" PV

.. code-block:: shell

  In [1]: request.write(1)
  Out[1]: WriteNotifyResponse(data_type=<ChannelType.DOUBLE: 6>, data_count=1, status=CAStatusCode(name='ECA_NORMAL', code=0, code_with_severi
  ty=1, severity=<CASeverity.SUCCESS: 1>, success=1, defunct=False, description='Normal successful completion'), ioid=0)

  In [2]: response.read()
  Out[2]: ReadNotifyResponse(data=array([1.58086159e+09]), data_type=<ChannelType.DOUBLE: 6>, data_count=1, status=CAStatusCode(name='ECA_NORM
  AL', code=0, code_with_severity=1, severity=<CASeverity.SUCCESS: 1>, success=1, defunct=False, description='Normal successful completion'), i
  oid=1, metadata=None)



Device
==================
Simple mock motor record with three PVs: VAL, RBV and running.

.. autoclass:: caproto_sandbox.worker_thread_device.Device
  :members:

Server
==================
There are three python classes in the file. The "Server" is a caproto PVGroup class.

.. automodule:: caproto_sandbox.worker_thread_server.Server
  :members:
  :undoc-members:
  :show-inheritance:
