#!/usr/bin/env python3
#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import epics
import epics.wx
from logging import debug,warn,info,error


import wx

__version__ = "0.0.0" #initial

class Window(wx.Frame):

        title = "Simple DAQ GUI"

        def __init__(self):
            wx.Frame.__init__(self, None, wx.ID_ANY, title=self.title, style=wx.DEFAULT_FRAME_STYLE)
            self.panel=wx.Panel(self, -1, size = (300,75))
            self.Bind(wx.EVT_CLOSE, self.on_quit)

            self.init()
            self.SetBackgroundColour(wx.Colour(255,255,255))
            self.Centre()
            self.Show()

        def on_quit(self,event):
            """
            orderly exit of Panel if close button is pressed
            """
            self.Destroy()
            del self

        def init(self):
            """
            """
            sizer = wx.GridBagSizer(hgap = 5, vgap = 5)
            self.label ={}
            self.field = {}
            self.sizer = {}
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            topSizer = wx.BoxSizer(wx.VERTICAL)



            self.sizer[b'time'] = wx.BoxSizer(wx.HORIZONTAL)
            self.label[b'time'] = wx.StaticText(self.panel, label= 'time:', style = wx.ALIGN_CENTER)
            self.field[b'time'] = epics.wx.PVText(self.panel, pv='simple_daq:TIME',minor_alarm = wx.Colour(5, 6, 7),auto_units = True, size = (100,20))
            self.sizer[b'time'].Add(self.label[b'time'] , 0)
            self.sizer[b'time'].Add(self.field[b'time'] , 0)


            self.sizer[b'cpu'] = wx.BoxSizer(wx.HORIZONTAL)
            self.label[b'cpu'] = wx.StaticText(self.panel, label= 'cpu:', style = wx.ALIGN_CENTER)
            self.field[b'cpu'] = epics.wx.PVText(self.panel, pv='simple_daq:CPU',minor_alarm = wx.Colour(5, 6, 7),auto_units = True, size = (100,20))
            self.sizer[b'cpu'].Add(self.label[b'cpu'] , 0)
            self.sizer[b'cpu'].Add(self.field[b'cpu'] , 0)


            self.sizer[b'memory'] = wx.BoxSizer(wx.HORIZONTAL)
            self.label[b'memory'] = wx.StaticText(self.panel, label= 'memory:', style = wx.ALIGN_CENTER)
            self.field[b'memory'] = epics.wx.PVText(self.panel, pv='simple_daq:MEMORY',minor_alarm = wx.Colour(5, 6, 7),auto_units = True, size = (100,20))
            self.sizer[b'memory'].Add(self.label[b'memory'] , 0)
            self.sizer[b'memory'].Add(self.field[b'memory'] , 0)

            self.sizer[b'battery'] = wx.BoxSizer(wx.HORIZONTAL)
            self.label[b'battery'] = wx.StaticText(self.panel, label= 'battery:', style = wx.ALIGN_CENTER)
            self.field[b'battery'] = epics.wx.PVText(self.panel, pv='simple_daq:BATTERY',minor_alarm = wx.Colour(5, 6, 7),auto_units = True, size = (100,20))
            self.sizer[b'battery'].Add(self.label[b'battery'] , 0)
            self.sizer[b'battery'].Add(self.field[b'battery'] , 0)

            self.sizer[b'update freq'] = wx.BoxSizer(wx.HORIZONTAL)
            self.label[b'update freq'] = wx.StaticText(self.panel, label= 'update freq. (s):', style = wx.ALIGN_CENTER)
            self.field[b'update freq'] = epics.wx.PVTextCtrl(self.panel, pv='simple_daq:dt', size = (100,20))
            self.sizer[b'update freq'].Add(self.label[b'update freq'] , 0)
            self.sizer[b'update freq'].Add(self.field[b'update freq'] , 0)

            main_sizer.Add(self.sizer[b'time'],0)
            main_sizer.Add(self.sizer[b'cpu'],0)
            main_sizer.Add(self.sizer[b'memory'],0)
            main_sizer.Add(self.sizer[b'battery'],0)
            main_sizer.Add(self.sizer[b'update freq'],0)



            self.Center()
            self.Show()
            topSizer.Add(main_sizer,0)


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
    panel = Window()

    app.MainLoop()
