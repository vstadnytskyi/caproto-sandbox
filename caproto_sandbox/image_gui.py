#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import epics
import epics.wx
from logging import debug,warn,info,error
from pdb import pm

import wx

__version__ = "0.0.0" #initial

class PanelTemplate(wx.Frame):

        title = "GUI Panel Template"


        def __init__(self):
            wx.Frame.__init__(self, None, wx.ID_ANY, title=self.title, style=wx.DEFAULT_FRAME_STYLE)
            self.panel=wx.Panel(self, -1)
            self.Bind(wx.EVT_CLOSE, self.OnQuit)


            self.initialize_GUI()
            self.SetBackgroundColour(wx.Colour(255,255,255))
            self.Centre()
            self.Show()

        def OnQuit(self,event):
            """
            orderly exit of Panel if close button is pressed
            """
            self.Destroy()
            del self

        def initialize_GUI(self):
            """
            """
            sizer = wx.GridBagSizer(hgap = 10, vgap = 10)
            self.labels ={}
            self.fields = {}
            self.sizers = {}
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            topSizer = wx.BoxSizer(wx.HORIZONTAL)

            image_sizer = wx.StaticBoxSizer(orient = wx.VERTICAL, parent = self.panel, label = 'Microscope Camera')
            self.sizers['image_mean'] = wx.BoxSizer(wx.HORIZONTAL)
            self.labels['image_mean']  = wx.StaticText(self.panel, label= 'image mean', style = wx.ALIGN_CENTER)
            self.fields['image_mean']  = epics.wx.PVText(self.panel, pv='TEST.image_mean',minor_alarm = wx.Colour(5, 6, 7),auto_units = True)
            self.sizers['image_mean'] .Add(self.labels['image_mean']  , 0)
            self.sizers['image_mean'] .Add(self.fields['image_mean']  , 0)

            self.sizers['image'] = wx.BoxSizer(wx.VERTICAL)
            self.labels['image']  = wx.StaticText(self.panel, label= 'Microscope Camera', style = wx.ALIGN_CENTER)
            self.fields['image']  = epics.wx.PVImage(self.panel, pv='TEST.image', im_size = (100,100))
            self.sizers['image'] .Add(self.labels['image']  , 0)
            self.sizers['image'] .Add(self.fields['image']  , 0)

            image_sizer.Add(self.sizers['image_mean'] ,0)
            image_sizer.Add(self.sizers['image'] ,0)

            topSizer.Add(image_sizer,0)

            self.Center()
            self.Show()

            self.panel.SetSizer(topSizer)
            topSizer.Fit(self)
            self.Layout()
            self.panel.Layout()
            self.panel.Fit()
            self.Fit()

if __name__ == '__main__':
    from pdb import pm
    import logging
    from tempfile import gettempdir


    app = wx.App(redirect=False)
    panel = PanelTemplate()

    app.MainLoop()
