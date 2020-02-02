#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from caproto.sync.client import read, write


class SyncClient():
    def __init__(self,prefix):
        self.prefix = prefix

    def get_RBV(self):
        from caproto.sync.client import read
        value = read(self.prefix + 'RBV')
        return value
    RBV = property(get_RBV)

    def get_VAL(self):
        from caproto.sync.client import read
        value = read(self.prefix + 'VAL')
        return value
    def set_VAL(self, value):
        from caproto.sync.client import write
        write(self.prefix + 'VAL', value)
    VAL = property(get_VAL,set_VAL)

motor = SyncClient(prefix = "BEAMLINE:motor.")

if __name__ == '__main__':
    pass
