#!/usr/bin/env python

import wx
import sys, string, os, glob, csv
import arcgisscripting
from datetime import datetime 
from lib.utils import *
import wx.lib.filebrowsebutton
from lib.progress import Progress
from lib.import_stops_from_RW_endpage import Import_Stops_from_RW_endpage

class Export_Stops_to_RW_Page(wx.Panel):

    def __init__(self, wizard, parent ):
        logging.debug("initiating Export stops to RW page")
        wx.Panel.__init__(self, parent = parent)

        self.export_stops_picker = None
        self.save_stops_picker = None
        self.wizard = wizard
        
        self.SetBackgroundColour(bg_color())

        body_sizer = wx.BoxSizer(orient = wx.VERTICAL)
        self.SetSizer(body_sizer)

        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        explain = wx.StaticText(self, -1, 'BLAH')
        explain.SetFont(font)
        body_sizer.Add(explain, flag = wx.EXPAND | wx.ALL, border=5)

        body_sizer.AddSpacer(5)
        body_sizer.Add(wx.StaticLine(self, -1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT, border = 10)
        body_sizer.AddSpacer(5)

        control_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=5)
        control_sizer.AddGrowableCol(1)
        body_sizer.Add(item = control_sizer, flag = wx.EXPAND | wx.ALL, border = 5)


        control_sizer.Add(item = wx.StaticText(self, -1, ''))
        self.export_stops_picker = wx.lib.filebrowsebutton.FileBrowseButton(self, labelText="Select Stops file:", 
                fileMask="*.dbf", buttonText='Open')
        control_sizer.Add( item = self.export_stops_picker, flag=wx.EXPAND)


        control_sizer.Add(item = wx.StaticText(self, -1, ''))
        self.save_stops_picker = wx.lib.filebrowsebutton.FileBrowseButton(self, labelText="Save New Customer file as:", 
                fileMask="*.csv", fileMode=2, buttonText='Save')
        control_sizer.Add( item = self.save_stops_picker, flag=wx.EXPAND)
        

        body_sizer.AddStretchSpacer()

        next = wx.Button(self, wx.ID_OK, 'Next')
        next.Bind(wx.EVT_BUTTON, self.OnNext) 
        body_sizer.Add(next, flag = wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL, border=10)


    def OnNext(self, event):
        logging.debug("customer file is: "+self.export_stops_picker.GetValue())        
        logging.debug("ready to open progress")

        self.wizard.next(Progress, message = 'Processing.....')        
        os.chdir(self.wizard.cwd)
        # Create the geoprocessor object
        gp = arcgisscripting.create() 
        Stops = (self.export_stops_picker.GetValue())
        # Set the workspace for the processing files
        gp.workspace = os.path.dirname(Stops)        
    




















