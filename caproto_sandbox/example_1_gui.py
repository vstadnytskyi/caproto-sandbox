#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Very simple graphical user interface.
- 'Dropdown' menu is an indicator and a selector for saved motor position
- "jog button" tweaks a motor value by a tweak value one way and back.
- static text field shows current RBV value
- "control float field" allows interaction with VAL PV

Rules:
the inserted state has position of 0
the retracted state has position of 1 

"""

import wx
import epics
import epics.wx
from logging import debug,warn,info,error

__version__ = "0.0.0" #initial
prefix = 'BEAMLINE:SERVER.'
class PanelTemplate(wx.Frame):

        title = "Example 1: Control Panel"

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
            main_sizer = wx.BoxSizer(wx.HORIZONTAL)
            sizer_1 = wx.BoxSizer(wx.VERTICAL)
            sizer_2 = wx.BoxSizer(wx.VERTICAL)
            sizer_3 = wx.BoxSizer(wx.VERTICAL)
            sizer_4 = wx.BoxSizer(wx.VERTICAL)
            sizer_5 = wx.BoxSizer(wx.VERTICAL)
            sizer_6 = wx.BoxSizer(wx.VERTICAL)
            sizer_7 = wx.BoxSizer(wx.VERTICAL)

            choices_label = wx.StaticText(self.panel, label = 'Choices')
            choices_field = epics.wx.PVEnumChoice(self.panel, pv = prefix + 'choices', size = (180,40))
            jog_button = epics.wx.PVButton(self.panel, pv = 'BEAMLINE:SERVER.jog', label = 'Jog', pushValue=1.0, disablePV='BEAMLINE:SERVER.jog', disableValue=1.0, size = (180,40))
            motors_rbv_label = wx.StaticText(self.panel, label = 'Motor 1: RBV')
            motors_rbv_field = epics.wx.PVText(self.panel, pv = 'BEAMLINE:motor.RBV', size = (180,40))
            motors_val_label = wx.StaticText(self.panel, label = 'Motor 1: VAL')
            motors_val_field = epics.wx.PVFloatCtrl(self.panel, pv = 'BEAMLINE:motor.VAL', size = (180,40))

            sizer_1.Add(choices_label,0, wx.ALIGN_CENTER, 0)
            sizer_1.Add(choices_field,0, wx.ALIGN_CENTER, 0)
            sizer_1.Add(jog_button,0, wx.ALIGN_CENTER, 0)
            sizer_1.Add(motors_rbv_label,0, wx.ALIGN_CENTER, 0)
            sizer_1.Add(motors_rbv_field,0, wx.ALIGN_CENTER, 0)
            sizer_1.Add(motors_val_label,0, wx.ALIGN_CENTER, 0)
            sizer_1.Add(motors_val_field,0, wx.ALIGN_CENTER, 0)


            main_sizer.Add(sizer_1,5, wx.ALL|wx.ALIGN_TOP, 5)
            main_sizer.Add(sizer_6,5, wx.ALL|wx.ALIGN_TOP, 5)


            self.panel.SetSizer(main_sizer)
            main_sizer.Fit(self)
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
