Disclaimer:
I am not a developer of the caproto library, I am a user. Here I describe my vision and understanding of the structure of caproto server from a user point of view. I am also hoping to provide some organization solutions. 

**************************************************
Principle of design and operation of CA server
**************************************************
In this section I want to break down the typical caproto server code into pieces. Press this link if you want to jump directly to `the final code <#final-code>`_

The caproto server consists of three main parts:

- `part 1:  <#part-1-definition-of-pvs>`_ definition of Process Variables (PVs)

- Initialization of async put and get queues

- Definition of Putter and Getter functions


Part 1: Definition of PVs
===============================
PVs can be conveniently defined at the very beginning of the class definition.

.. code-block:: python

    class Server(PVGroup):
      running = pvproperty(value=1)
      rbv = pvproperty(value = 0.0)
      val = pvproperty(value = 0.0)

this simple code will create two PVs with some initial values. The rbv (read-back value) and val (set value) resemble standard names for a typical motor record. In my code, I have added an extra PV 'running' the purpose of which will be discussed later.


Part 2: Async Queues
===============================

Next we need to define asynchronous (async) queue that are used to safely pass calls between asynchronous caproto server and other objects that can be traditional threads. The 'async def running():' defines an async function. The decorator @running.startup marks this function as the one that will be executed upon startup of the 'running' PV. Inside of this function we will create asynchronous put and get queues.

.. code-block:: python

  @running.startup
  async def running(self, instance, async_lib):
      'Periodically update the value'
      self.running.write(1)
      self.put_queue = async_lib.ThreadsafeQueue()
      self.get_queue = async_lib.ThreadsafeQueue()

The important part of the caproto server design is the following while loop. This loop is defined in the @running.startup function

.. code-block:: python

  while True:
              entry = await self.put_queue.async_get()

This line will asynchronously wait for a new entry in the put_queue.

Part 3: Putters and Getters
===============================
The rest of the code defines what function will be executed when put(write) and get(read) into a specified PV. The decorator '@val.putter' shows that the following function will be executed when a 'put' or 'write' request arrives for the 'val' PV.

.. code-block:: python

      @val.putter
      async def val(self, instance, value):

The decorator '@val.getter' indicates that the following function will be executed when a 'get' or 'read' request arrives for the 'val' PV.

.. code-block:: python

      @val.getter
      async def val(self, instance, value):


Final code
===============================

.. literalinclude:: ../../caproto_sandbox/simple_server.py
