#!/usr/bin/env python3
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    from caproto.threading.client import Context

    default_prefix='TEST:PUTTER.'
    ctx = Context()
    bit,set_bit = ctx.get_pvs(default_prefix+'bit',default_prefix+'set_bit')
