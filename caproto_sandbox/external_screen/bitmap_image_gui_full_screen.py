#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import epics
import epics.wx
from logging import debug,warn,info,error
from pdb import pm

import os
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = '48000096' #there is a limit of how big PV can be on the client size. This overrrides that limitation.

from icarus_nmr.pyepics import PVImage

__version__ = "0.0.0" #initial

class MyPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        self.Bind(wx.EVT_KEY_DOWN, self.onKey)
        self.SetBackgroundColour((0, 0, 0))

    def onKey(self, event):
        """
        Check for ESC key press and exit is ESC is pressed
        """
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            self.GetParent().Close()
        else:
            event.Skip()
class MyFrame(wx.Frame):
    """"""

    def __init__(self):
        """Constructor"""   
        wx.Frame.__init__(self, None, title="Test FullScreen")
        self.panel = MyPanel(self)
        self.initialize_GUI()
        self.SetBackgroundColour(wx.Colour(255,255,255))
        self.ShowFullScreen(True)

    def initialize_GUI(self):
        """
        """

        width = 1920#1920 #int(1920/2)
        height = 1080 #1080#int(1080/2)

        sizer = wx.GridBagSizer(hgap = 10, vgap = 10)
        self.labels ={}
        self.fields = {}
        self.sizers = {}
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.sizers['image'] = wx.BoxSizer(wx.VERTICAL)
        
        self.fields['image']  = PVImage(self.panel, pv='BITMAP_IMAGE:image', im_size = (width,height))
        self.sizers['image'] .Add(self.fields['image']  , 0)

        self.panel.SetSizer(topSizer)

if __name__ == '__main__':
    from pdb import pm
    import logging
    from tempfile import gettempdir

    app = wx.App(False)
    frame = MyFrame()
    frame.SetPosition((-800,-1000))
    frame.Maximize()
    app.MainLoop()