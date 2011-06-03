#!/usr/bin/env python newfile

import wx
import os, sys
from lib.utils import *
from lib.ra_params_page import RA_Params_Page



class Choose_Export_Files_Page(wx.Panel):

    def __init__(self, wizard, parent ):
        logging.debug("initiating")
        wx.Panel.__init__(self, parent = parent)

        self.customer_file_picker = None
        self.vehicle_file_picker = None
        self.facility_file_picker = None
        self.wizard = wizard
        
        self.SetBackgroundColour(bg_color())

        body_sizer = wx.BoxSizer(orient = wx.VERTICAL)
        self.SetSizer(body_sizer)

        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        explain = wx.StaticText(self, -1, 'Create and export files from FleetRoute to RouteApp. \n'
                      +' \n'          
                      +'You will need to select your facility, vehicles and stops datbase tables\n'
                      +'from your default shapefiles.')
        explain.SetFont(font)
        body_sizer.Add(explain, flag = wx.EXPAND | wx.ALL, border=5)

        body_sizer.AddSpacer(5)
        body_sizer.Add(wx.StaticLine(self, -1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT, border = 10)
        body_sizer.AddSpacer(5)

        control_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=5)
        control_sizer.AddGrowableCol(1)
        body_sizer.Add(item = control_sizer, flag = wx.EXPAND | wx.ALL, border = 5)

        picker_open_style = wx.FLP_OPEN | wx.FLP_FILE_MUST_EXIST | wx.FLP_CHANGE_DIR

        control_sizer.Add(item = wx.StaticText(self, -1, 'Facility File.dbf:'))
        self.facility_file_picker = wx.FilePickerCtrl(self, message='Choose the Facility.dbf', 
                wildcard='*.dbf', style= picker_open_style)
        control_sizer.Add( item = self.facility_file_picker, flag=wx.EXPAND)

        control_sizer.Add(item = wx.StaticText(self, -1, 'Vehicle File.dbf:'))
        self.vehicle_file_picker = wx.FilePickerCtrl(self, message = 'Choose the Vehicle.dbf',
                wildcard='*.dbf', style= picker_open_style)
        control_sizer.Add( item = self.vehicle_file_picker, flag=wx.EXPAND)
        
        control_sizer.Add(item = wx.StaticText(self, -1, 'Customer File.dbf:'))
        self.customer_file_picker = wx.FilePickerCtrl(message = 'Choose the Customer.dbf', parent=self, 
            wildcard='*.dbf', style= picker_open_style)
        control_sizer.Add( item = self.customer_file_picker, flag=wx.EXPAND)

        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.gotEverything)

        # widgets for tool        

        body_sizer.AddStretchSpacer()

        next = wx.Button(self, wx.ID_OK, 'Next')
        next.Disable()
        next.Bind(wx.EVT_BUTTON, self.OnRun) 
        body_sizer.Add(next, flag = wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL, border=10)
       
    def OnRun(self, event):
        logging.debug("customer dbf"+self.customer_file_picker.GetPath())        
        self.wizard.next(RA_Params_Page,
                         customer_file = self.customer_file_picker.GetPath(),                         
                         vehicle_file = self.vehicle_file_picker.GetPath(),
                         facility_file = self.facility_file_picker.GetPath()
                         )

     
    def gotEverything(self,event) :
        ok_button = self.FindWindowById(wx.ID_OK)
        if (self.customer_file_picker.GetPath() == '' 
                or self.vehicle_file_picker.GetPath() == ''
                or self.facility_file_picker.GetPath() == ''
                ):
            ok_button.Disable()
        else :
            ok_button.Enable()
