from caproto.threading.client import Context
prefix='bitmap_generator:'
ctx = Context()
t1, = ctx.get_pvs(prefix+'t1')
shape, = ctx.get_pvs(prefix+'shape')
image, = ctx.get_pvs(prefix+'image')
