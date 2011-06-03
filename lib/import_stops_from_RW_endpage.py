#!/usr/bin/env python

import wx
import os, sys
from lib.utils import *


class Import_Stops_from_RW_endpage(wx.Panel):
    
    def __init__(self, wizard, parent, stops_file):
        logging.debug("initiating Import Stops from RW end page")
        wx.Panel.__init__(self, parent = parent)
        
        self.wizard = wizard
        self.stops_file = stops_file

        self.SetBackgroundColour(bg_color())

        body_sizer = wx.BoxSizer(orient = wx.VERTICAL)
        self.SetSizer(body_sizer)

        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        explain = wx.StaticText(self, -1, 'BLAH BLAH')
        explain.SetFont(font)
        body_sizer.Add(explain, flag = wx.EXPAND | wx.ALL, border=5)

        body_sizer.AddSpacer(5)
        body_sizer.Add(wx.StaticLine(self, -1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT, border = 10)
        body_sizer.AddSpacer(5)

        control_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=5)
        control_sizer.AddGrowableCol(1)
        body_sizer.Add(item = control_sizer, flag = wx.EXPAND | wx.ALL, border = 5)


        control_sizer.Add(item = wx.StaticText(self, -1, 'Your new customer file is:  \n'
                                               +self.stops_file))

        body_sizer.AddStretchSpacer()

        next = wx.Button(self, wx.ID_OK, 'Exit')
        next.Bind(wx.EVT_BUTTON, self.OnClose) 
        body_sizer.Add(next, flag = wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL, border=10)
        
       
    def OnClose(self, event):
        logging.debug("completed end page....")
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
        