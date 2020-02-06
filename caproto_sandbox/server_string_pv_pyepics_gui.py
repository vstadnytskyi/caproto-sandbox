#!/usr/bin/env python3
#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import epics
import epics.wx
from logging import debug,warn,info,error


import wx

__version__ = "0.0.0" #initial
prefix='simple_str:'
class PanelTemplate(wx.Frame):

        title = "GUI Panel Template"

        def __init__(self):
            wx.Frame.__init__(self, None, wx.ID_ANY, title=self.title, style=wx.DEFAULT_FRAME_STYLE)
            self.panel=wx.Panel(self, -1, size = (200,75))
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
            sizer = wx.GridBagSizer(hgap = 5, vgap = 5)
            self.label ={}
            self.field = {}
            self.sizer = {}
            main_sizer = wx.BoxSizer(wx.VERTICAL)
            topSizer = wx.BoxSizer(wx.VERTICAL)



            self.sizer[b'str_in'] = wx.BoxSizer(wx.VERTICAL)
            self.label[b'str_in'] = wx.StaticText(self.panel, label= 'str_in:', style = wx.ALIGN_CENTER)
            self.field[b'str_in'] = epics.wx.PVText(self.panel, pv=prefix+'str_in',minor_alarm = wx.Colour(5, 6, 7),auto_units = True)
            self.sizer[b'str_in'].Add(self.label[b'str_in'] , 0)
            self.sizer[b'str_in'].Add(self.field[b'str_in'] , 0)

            self.sizer[b'str_out'] = wx.BoxSizer(wx.VERTICAL)
            self.label[b'str_out'] = wx.StaticText(self.panel, label= 'str_out:', style = wx.ALIGN_CENTER)
            self.field[b'str_out'] = epics.wx.PVText(self.panel, pv=prefix+'str_out',minor_alarm = wx.Colour(5, 6, 7),auto_units = True)
            self.sizer[b'str_out'].Add(self.label[b'str_out'] , 0)
            self.sizer[b'str_out'].Add(self.field[b'str_out'] , 0)

            self.sizer[b'str_in_control'] = wx.BoxSizer(wx.VERTICAL)
            self.label[b'str_in_control'] = wx.StaticText(self.panel, label= 'str_in_control:', style = wx.ALIGN_CENTER)
            self.field[b'str_in_control'] = epics.wx.PVTextCtrl(self.panel, pv='NIH:SYRINGE1.VALVE')
            self.sizer[b'str_in_control'].Add(self.label[b'str_in_control'] , 0)
            self.sizer[b'str_in_control'].Add(self.field[b'str_in_control'] , 0)

            self.sizer[b'str_in_control2'] = wx.BoxSizer(wx.VERTICAL)
            self.label[b'str_in_control2'] = wx.StaticText(self.panel, label= 'str_in_control2:', style = wx.ALIGN_CENTER)
            self.field[b'str_in_control2'] = epics.wx.PVTextCtrl(self.panel, pv=prefix+'str_in2')
            self.sizer[b'str_in_control2'].Add(self.label[b'str_in_control2'] , 0)
            self.sizer[b'str_in_control2'].Add(self.field[b'str_in_control2'] , 0)

            self.sizer[b'N_chr'] = wx.BoxSizer(wx.VERTICAL)
            self.label[b'N_chr'] = wx.StaticText(self.panel, label= 'N_chr:', style = wx.ALIGN_CENTER)
            self.field[b'N_chr'] = epics.wx.PVText(self.panel, pv=prefix+'N_chr',minor_alarm = wx.Colour(5, 6, 7),auto_units = True)
            self.sizer[b'N_chr'].Add(self.label[b'N_chr'] , 0)
            self.sizer[b'N_chr'].Add(self.field[b'N_chr'] , 0)

            main_sizer.Add(self.sizer[b'str_in'],0)
            main_sizer.Add(self.sizer[b'str_out'],0)
            main_sizer.Add(self.sizer[b'str_in_control'],0)
            main_sizer.Add(self.sizer[b'str_in_control2'],0)
            main_sizer.Add(self.sizer[b'N_chr'],0)


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
    panel = PanelTemplate()

    app.MainLoop()
