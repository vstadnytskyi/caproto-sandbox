=====================================
Example Simple Data Acquisition Unit
=====================================

This is an example of a simple data acquisition unit. The data comes from your computer onboard sensors e.g.: CPU utilization, battery capacity and memory utilization.

The example is purposely divided into several different files to explicitly show the modularity and hierarchy. The files are: **driver**, **device**, **server**, **gui**, and **client**.

.. figure::  ../images/simple_device.jpeg
   :align:   center

The **driver** file contains one Driver class. The instantiation of the class connects to a data acquisition unit(this case on-board sensors) and through  a simple read() function provides higher level command to retrieve data from sensors. The result is returned as a numpy array, in this case 1x4 with entries sorted as following: time, CPU utilization in %, memory utilization in GB, battery capacity in %.

The next level in the hierarchy is **device** level. The device code consists of one Device class. The initialization of the device instance creates circular buffer where the data from the data acquisition unit will be stored. This example does not take advantage of the circular buffer explicitly, but it can be used to expand the example in future and add more fields like mean CPU usage, etc. The purpose of the device class is to collect data on a clock and put it in circular buffer.

The **server** code puts entire example on the network using caproto library. The server level has six Process Variables(PVs):  TIME, CPU, MEMORY, BATTERY, dt, LIST
- TIME - time of last read (UnixTime)
- CPU - CPU utilization value during last read
- MEMORY - MEMORY utilization value during last read
- BATTERY - BATTERY utilization value during last read
- dt - update frequency in seconds
- LIST - combined PV that transmits all data acquired during last data acquisition

The **GUI** code uses wxPython in combination with PyEpics. The GUI code is heavily utilizing wxPython BoxSizers to make the code modular and hierarchical.

The **client** code is a simple example of line based communications. This example can be incorporate into a higher level IOCs that can talk to the lower level IOCs without GUI interface.

Example of usage
==================

You would need to open multiple terminal tabs in one window. But first start terminal and change directory to the location of the library.

to test the driver code:

.. code-block:: python

  from caproto_sandbox.simple_daq.driver import Driver
  driver = Driver()
  driver.read()

  .. code-block:: python

    from caproto_sandbox.simple_daq.device import Device
    driver = Driver()
    device = Device(driver = driver)
    device.driver.read()
    device.buffer.pointer
    -1
    device.run_once()  
    device.buffer.pointer
    0

Driver
==================
Simple data acquisition driver example.

.. autoclass:: caproto_sandbox.simple_daq.driver.Driver
  :members:
  :undoc-members:
  :show-inheritance:

Device
==================
Simple data acquisition device example.

.. autoclass:: caproto_sandbox.simple_daq.device.Device
  :members:
  :undoc-members:
  :show-inheritance:

Server (CA IOC)
==================
Simple data acquisition device example.

.. autoclass:: caproto_sandbox.simple_daq.server.Server
  :members:
  :undoc-members:
  :show-inheritance:

Graphical User Interface
==========================
Graphical user interface module written in PyEpics and wxPython

.. autoclass:: caproto_sandbox.simple_daq.gui.Window
  :members:
  :undoc-members:
  :show-inheritance:

Client
==========================
The line base client written in caproto

.. autoclass:: caproto_sandbox.simple_daq.client.Client
  :members:
  :undoc-members:
  :show-inheritance:
