#!/usr/bin/env python

import wx
import os, sys
from lib.utils import *

class Progress(wx.Panel):

    def __init__(self, wizard, parent, message, cancel_text = "Cancel", cancel_action = None):
        logging.debug("initiating progress")
        wx.Panel.__init__(self, parent = parent)

        self.wizard = wizard
        
        self.SetBackgroundColour(bg_color())

        body_sizer = wx.BoxSizer(orient = wx.VERTICAL)
        self.SetSizer(body_sizer)

        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        explain = wx.StaticText(self, -1, message)
        explain.SetFont(font)
        body_sizer.Add(explain, flag = wx.EXPAND | wx.ALL, border=5)

        # widgets for tool        

        if cancel_action:
            body_sizer.AddStretchSpacer()

            next = wx.Button(self, wx.ID_CANCEL, cancel_text)
            next.Bind(wx.EVT_BUTTON, cancel_action, next) 
            body_sizer.Add(next, flag = wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL, border=10)

    @staticmethod
    def exit(event):
        logging.debug("exit selected")
        # convenience method
        exit(1)
