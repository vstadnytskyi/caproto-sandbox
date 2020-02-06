=======================
Example Simple Device
=======================

Consists of:

1) Server
2) Client
3) Device

The worker_thread_device code is a simple example of a device code. The device returns current time. This operation takes 0.2s. The return value is submitted to response_queue and will be taken care by the Server.

The server code has two PVs: request and response. An event of writing into request PV triggers a spawn of new thread that requests time from the device. The response from device gets published into response PV.

The client code is a simple example of client that allows you to submit a time request and get a response.

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
