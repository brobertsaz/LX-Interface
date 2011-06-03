#!/usr/bin/env python

import wx
import os, sys
import arcgisscripting
from wx.lib.wordwrap import wordwrap
from lib.utils import *
from lib.progress import Progress
from gzip import GzipFile 
from ra_xl import RA_Routes_Sheet
from end_page import End_Page


class Update_Sequence_Page(wx.Panel):
    
    def __init__(self, wizard, parent, copy_customers_dbf, spreadsheet):
        logging.debug("Update the route/sequence in "+copy_customers_dbf)
        wx.Panel.__init__(self, parent = parent)
        
        self.wizard = wizard
        self.copy_customers_dbf = copy_customers_dbf
        self.spreadsheet = spreadsheet

        self.SetBackgroundColour = (bg_color())

        body_sizer = wx.BoxSizer(orient = wx.VERTICAL)
        self.SetSizer(body_sizer)

        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        explain = wx.StaticText(self, -1, 'Your results from the C2RouteApp have downloaded. \n'
                                +'Click "Finish" to update your customers with the new route and/or sequence \n'
                                +'number and create your final customer file.')
        explain.SetFont(font)
        body_sizer.Add(explain, flag = wx.EXPAND | wx.ALL, border=5)

        body_sizer.AddSpacer(5)
        body_sizer.Add(wx.StaticLine(self, -1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT, border = 10)
        body_sizer.AddSpacer(5)

        control_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=5)
        control_sizer.AddGrowableCol(1)
        body_sizer.Add(item = control_sizer, flag = wx.EXPAND | wx.ALL, border = 5)

        control_sizer.Add(item = wx.StaticText(self, -1, 'Your file has downloaded:  \n'
                                               +spreadsheet))

        body_sizer.AddStretchSpacer()

        next = wx.Button(self, wx.ID_OK, 'Finish')
        next.Bind(wx.EVT_BUTTON, self.Process) 
        body_sizer.Add(next, flag = wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL, border=10)
        
       
    def Process(self, event):
        self.wizard.next(Progress, message = "Updating %s with route/sequence..." % self.copy_customers_dbf)

        logging.debug("start dbf update")
        gp = arcgisscripting.create(9.3)
        gp.workspace = (self.copy_customers_dbf)

        # f_out = open(self.spreadsheet+".xls", 'wb')
        # f_in = GzipFile(self.spreadsheet,'rb')

        # f_out.writelines(f_in)
        # f_out.close()
        # f_in.close()

        sheet = RA_Routes_Sheet(self.spreadsheet)


        # This is to process new routes created
        # We will have a 2nd process to update just the sequence
        for row in sheet :
            if row['customer_name']== '' or row['customer_name']== None: continue
            logging.debug("Site_id == %s" % row['customer_name'])
            dbf_cursor = gp.UpdateCursor(self.copy_customers_dbf, "Site_id = %s" % row['customer_name'])
            dbf_row = dbf_cursor.Next()

            # Fix this to update the right columns
            # 'row' is a dict. print inspect(row) to see it
            # 'dbf_row' has instance-variables for the fields,
            # the fields are given by print inspect(gp.ListFields(table_view))
            dbf_row.Sequence = row['ts_stop_position']
            dbf_row.Route = row['vehicle_id']
            dbf_row.Est_toa = row['ts_stop_start_time']

            dbf_cursor.UpdateRow(dbf_row)
            dbf_row = dbf_cursor.Next()
            del dbf_cursor

        logging.debug("Done updating dbf")
        
        self.wizard.next(End_Page, copy_customers_dbf = self.copy_customers_dbf)        

