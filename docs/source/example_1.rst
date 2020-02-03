============
Example 1
============

Consists of:

1) Mock motor record

2) Server (middle man)

3) GUI

4) Client

Mock motor record
==================
Simple mock motor record with three PVs: VAL, RBV and running.

.. autoclass:: caproto_sandbox.example_1_motor.Server
  :members:

Server
==================
There are three python classes in the file. The "Server" is a caproto PVGroup class and Choices, Motors are client classes that provide simple interface.

.. autoclass:: caproto_sandbox.example_1_server.Server
  :members:

.. autoclass:: caproto_sandbox.example_1_server.Choices
  :members:

The Motors class has two PVs hard-coded: BEAMLINE:motor.RBV and BEAMLINE:motor.VAL. it subscribes to PVs and act if new values is posted. The
arrival of new value calls a callback function.

.. autoclass:: caproto_sandbox.example_1_server.Motors
  :members:
