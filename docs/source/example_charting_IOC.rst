====================
Example "Charting IOC"
====================

This is an example of a soft IOC that takes some data and charts it with matplotlib. The figure is available as a bitmap image that can be broadcasted by Channel Access. The chart_generator_GUI has a field which is a simple bitmap of a given size. This is a way to offload the plotting burden to a softIOC and simplify GUI. The GUI will just have a PVImage object from the modified pyepics library.


Consists of:

1) Mock motor record (example_1_motor.py)

2) Server (middle man) (example_1_server.py)

3) GUI (example_1_gui.py)

4) Client (example_1_client.py)

Two codes need to be running in to different shells\terminals. make sure to change directory to the directory with example_1 codes.

Two start a mock motors

.. code-block:: shell

    run example_1_motor.py

You should see something similar to the following 5 lines:

.. code-block:: shell

    [[User user$ ipython3 caproto_sandbox/example_1_motor.py
    [I 00:54:27.859          server:  162] Asyncio server starting up...
    [I 00:54:27.860          server:  175] Listening on 0.0.0.0:63591
    [I 00:54:27.861          server:  261] Server startup complete.
    * request method called at server startup @start.startup

The mock motor is running now. Next step, start the server.

.. code-block:: shell

    run example_1_server.py

.. code-block:: shell

    [I 00:57:13.714          server:  162] Asyncio server starting up...
    [I 00:57:13.715          server:  175] Listening on 0.0.0.0:50377
    [I 00:57:13.716          server:  261] Server startup complete.

To start Grahical user interface run the following command:

.. code-block:: shell

    run example_1_server.py

You will get a panel that looks like this;

.. image:: images/example_1_gui.png
  :width: 300px


Mock motor record
==================
Simple mock motor record with three PVs: VAL, RBV and running.

.. autoclass:: caproto_sandbox.example_1_motor.Server
  :members:

Server
==================
There are three python classes in the file. The "Server" is a caproto PVGroup class and Choices, Motors are client classes that provide simple interface.

.. automodule:: caproto_sandbox.example_1_server
  :members:
  :undoc-members:
  :show-inheritance:


The Motors class has two PVs hard-coded: BEAMLINE:motor.RBV and BEAMLINE:motor.VAL. it subscribes to PVs and act if new values is posted. The
arrival of new value calls a callback function.
