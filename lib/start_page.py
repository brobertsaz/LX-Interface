#!/usr/bin/env python

import wx
import os, sys
from lib.utils import *
from lib.progress import Progress
from lib.choose_export_files_page import Choose_Export_Files_Page
from lib.start_download_page import Start_Download_Page
from lib.import_stops_from_RW_page import Import_Stops_from_RW_Page
#from lib.import_streets_from_SDE_page import Import_Streets_from_SDE_Page
from lib.export_stops_to_RW_page import Export_Stops_to_RW_Page
#from lib.edit_params_page import Edit_Params_Page


class Start_Page(wx.Panel):

    def __init__(self, wizard, parent):
        logging.debug("initiating")
        wx.Panel.__init__(self, parent = parent)

        self.wizard = wizard

        self.SetBackgroundColour(bg_color())

        self.body_sizer = wx.BoxSizer(orient = wx.VERTICAL)
        self.SetSizer(self.body_sizer)

        explain = wx.StaticText(self, -1, 'BLAH')
        
        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        explain.SetFont(font)
        self.body_sizer.Add(explain, flag = wx.EXPAND | wx.ALL, border=10)

        self.body_sizer.AddSpacer(5)
        self.body_sizer.Add(wx.StaticLine(self, -1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT, border = 15)
        self.body_sizer.AddSpacer(5)

        control_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=5)
        control_sizer.AddGrowableCol(1)
        self.body_sizer.Add(item = control_sizer, flag = wx.EXPAND | wx.ALL, border = 5)


        control_sizer.Add(item = wx.StaticText(self, -1, 'Import Stops to FleetRoute'))
        RW2FR = wx.Button(self, wx.ID_OK, 'Select')
        control_sizer.Add(item = RW2FR, flag = wx.ALIGN_CENTER_HORIZONTAL, border = 5)
        RW2FR.Bind(wx.EVT_BUTTON, self.Import_stops_from_RW)


        control_sizer.Add(item = wx.StaticText(self, -1, 'Import Streets to FleetRoute'))
        ST2FR = wx.Button(self, wx.ID_OK, 'Select')
        control_sizer.Add(item = ST2FR, flag = wx.ALIGN_CENTER_HORIZONTAL, border = 5)
        ST2FR.Bind(wx.EVT_BUTTON, self.Import_streets_from_SDE)

        
        control_sizer.Add(item = wx.StaticText(self, -1, 'Edit Stop Time and Weight Parameters'))
        Params = wx.Button(self, wx.ID_OK, 'Select')
        control_sizer.Add(item = Params, flag = wx.ALIGN_CENTER_HORIZONTAL, border = 5)
        Params.Bind(wx.EVT_BUTTON, self.Edit_Params)


        control_sizer.Add(item = wx.StaticText(self, -1, 'Export Stops to RouteWare'))
        FR2RW = wx.Button(self, wx.ID_OK, 'Select')
        control_sizer.Add(item = FR2RW, flag = wx.ALIGN_CENTER_HORIZONTAL, border = 5)
        FR2RW.Bind(wx.EVT_BUTTON, self.Export_stops_to_RW)


        control_sizer.Add(item = wx.StaticText(self, -1, 'Export from FleetRoute to C2RouteApp     '))
        RA2FR = wx.Button(self, wx.ID_OK, 'Select')
        control_sizer.Add(item = RA2FR, flag = wx.ALIGN_CENTER_HORIZONTAL, border = 5)
        RA2FR.Bind(wx.EVT_BUTTON, self.Export_from_FR)


        control_sizer.Add(item = wx.StaticText(self, -1, 'Import from C2RouteApp to FleetRoute     '))
        RA2FR = wx.Button(self, wx.ID_OK, 'Select')
        control_sizer.Add(item = RA2FR, flag = wx.ALIGN_CENTER_HORIZONTAL, border = 5)
        RA2FR.Bind(wx.EVT_BUTTON, self.Import_from_RA)          

    def Import_stops_from_RW(self, event):
        self.wizard.next(Import_Stops_from_RW_Page)

    def Import_streets_from_SDE(self,event) :
         self.wizard.next(Start_Download_Page)
         #self.wizard.next(Import_Streets_from_SDE_Page)

    def Edit_Params(self, event):
        self.wizard.next(Choose_Export_Files_Page)
        #self.wizard.next(Edit_Params_Page)

    def Export_stops_to_RW(self,event) :
         self.wizard.next(Export_Stops_to_RW_Page)

    def Export_from_FR(self, event):
        self.wizard.next(Choose_Export_Files_Page)

    def Import_from_RA(self,event) :
         self.wizard.next(Start_Download_Page)         

