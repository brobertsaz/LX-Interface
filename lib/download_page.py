#!/usr/bin/env python

import wx
import os, sys
from lib.utils import *
from lib.progress import Progress
from lib.route_app.download import Download
from update_sequence_page import Update_Sequence_Page

EVT_DOWNLOAD = wx.NewEventType()

class Download_Page(wx.Panel):

    def __init__(self, wizard, parent, project_id):
        logging.debug("initiating  monitor optimization page")
        wx.Panel.__init__(self, parent = parent)
        
        self.wizard = wizard
        self.project_id = project_id
        self.SetBackgroundColour(bg_color())

        body_sizer = wx.BoxSizer(orient = wx.VERTICAL)
        self.SetSizer(body_sizer)
        
        self.explain = wx.StaticText(self, -1, 'Checking....')       
        body_sizer.Add(self.explain, flag = wx.EXPAND | wx.ALL, border=5)

        body_sizer.AddStretchSpacer()

        # delay till out of __init__
        wx.CallAfter(self.start)

    def start(self):
        self.wizard.next(Progress, message = "Starting...")
        wx.CallAfter(self.check)

    def check(self):
        self.downer = Download(project_id = self.project_id)
        rez = self.downer.check(user = os.environ.get( "USERNAME" ))

        if rez['error']:
            self.wizard.next(Progress, message = "Error: %s" % rez['error'], cancel_text='Exit', cancel_action=Progress.exit)
            return

        user_data = rez['user_data1']
        self.dir = user_data['dir']
        self.copy_customers_dbf = user_data['copy_customers_dbf'] if 'copy_customers_dbf' in user_data else ''
        
        wx.CallAfter(self.download)

    def download(self):
        rez = self.downer.download(self.dir)
        logging.debug("file downloaded...")
        if rez['error']:
            self.wizard.next(Progress, message = "Error: %s" % rez['error'], cancel_text='Exit', cancel_action=Progress.exit)
            return

        logging.debug("dir = "+self.dir+self.copy_customers_dbf)
        self.wizard.next(Update_Sequence_Page, copy_customers_dbf = os.path.join(self.dir, self.copy_customers_dbf),spreadsheet = rez["filename"])
        logging.debug("after Update_Sequence_Page...")

        
