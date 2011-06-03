#!/usr/bin/env python

import wx
import os, sys
from lib.utils import *
from lib.progress import Progress
from lib.monitor_optimization_page import Monitor_Optimization_Page

try:
    import json
except ImportError:
    import simplejson as json

class Start_Download_Page(wx.Panel):
    
    def __init__(self, wizard, parent):
        logging.debug("initiating")
        wx.Panel.__init__(self, parent = parent)
        
        self.wizard = wizard
        self.SetBackgroundColour(bg_color())

        body_sizer = wx.BoxSizer(orient = wx.VERTICAL)
        self.SetSizer(body_sizer)

        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        explain = wx.StaticText(self, -1, 'Please enter the Project ID from your email confirmation. \n'
                                +'\n')
        explain.SetFont(font)
        body_sizer.Add(explain, flag = wx.EXPAND | wx.ALL, border=5)

        body_sizer.AddSpacer(5)
        body_sizer.Add(wx.StaticLine(self, -1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT, border = 10)
        body_sizer.AddSpacer(5)

        control_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=5)
        control_sizer.AddGrowableCol(1)
        body_sizer.Add(item = control_sizer, flag = wx.EXPAND | wx.ALL, border = 5)

        control_sizer.Add(item = wx.StaticText(self, -1, 'Project ID:'))
        self.project_id_box = wx.TextCtrl(self,-1,'')
        control_sizer.Add(item = self.project_id_box)
        
        body_sizer.AddStretchSpacer()

        finish = wx.Button(self, wx.ID_OK, 'Next')
        finish.Bind(wx.EVT_BUTTON, self.OnFinish) 
        body_sizer.Add(finish, flag = wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL, border=10)
        
    def OnFinish(self, event):
        if not self.project_id_box.GetValue():
            wx.MessageBox("Need a project id")           
        else:
            logging.debug("started processing")
            self.start_processing()

    def start_processing(self):
       self.wizard.next(Monitor_Optimization_Page, project_id= self.project_id_box.GetValue())
        
