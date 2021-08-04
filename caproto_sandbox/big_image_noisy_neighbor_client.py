from caproto.threading.client import Context

ctx = Context()
image, = ctx.get_pvs('big_image:image')

# def f(sub,response):
#     responses.append(response.data)
#
# sub = image.subscribe()
# token = sub.add_callback(f)

def test_iamge_read(image,N = 10):
    from time import time
    for i in range(N):
        t1 = time()
        arr = image.read().data
        t2 = time()
        print(t2-t1)
