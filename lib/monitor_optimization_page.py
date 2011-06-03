#!/usr/bin/env python

import wx
import os, sys
sys.path.append('.')
from wx.lib.wordwrap import wordwrap
from lib.utils import *
from lib.route_app.route import Route
from lib.progress import Progress
from lib.download_page import Download_Page

class Monitor_Optimization_Page(wx.Panel):

    def __init__(self, wizard, parent, project_id):
        logging.debug("initiating  monitor optimization page")
        wx.Panel.__init__(self, parent = parent)
        
        self.wizard = wizard
        self.project_id = project_id
        self.SetBackgroundColour(bg_color())

        body_sizer = wx.BoxSizer(orient = wx.VERTICAL)
        self.SetSizer(body_sizer)
        
        self.explain = wx.StaticText(self, -1, "Checking Project ID %s" % self.project_id)       
        body_sizer.Add(self.explain, flag = wx.EXPAND | wx.ALL, border=5)

        body_sizer.AddStretchSpacer()
        self.kill_button = wx.Button(self, -1, 'Cancel Optimization')
        self.kill_button.Disable()
        body_sizer.Add(self.kill_button, flag = wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL, border=10)
        self.Bind(wx.EVT_BUTTON, self.kill, self.kill_button)

        self.monitor = Route(project_id)
        rez = self.monitor.monitor(observer = lambda(s): self.update_status(s), seconds = 5, wait_initial = True)

    def kill(self, evt):
        self.kill_button.Disable()
        self.monitor.kill_optimization()

    def update_status(self, status):
        logging.debug("test status %s, done? %s" % (inspect(status), status['status'] in Route.Done_Status))
        if 'running' not in status:
            self.wizard.next(Progress, message = "There has been an error in routing: "+inspect(status), cancel_text = 'Exit', cancel_action = Progress.exit)
            return
        elif status['running'] == None:
            logging.debug("status running = none")
            self.monitor.cancel_monitor()
            self.wizard.next(Progress, message = "Not optimizing: "+inspect(status), 
                cancel_text = 'Exit', cancel_action = Progress.exit)

        elif status['status'] in Route.Done_Status:
            self.monitor.cancel_monitor()
            self.wizard.next(Progress, message = "Elapsed Time:  %s\n   Status: %s" % (status['elapsed'],status['status']),
                cancel_text = 'Download', cancel_action = self.download)

        elif status['stopped'] != None:
            self.monitor.cancel_monitor()

            self.wizard.next(Progress, message = " Elapsed Time:  %s\n Status: %s\n Routing: %s" % (status['elapsed'],status['status'], status['stopped']), cancel_text = 'Exit', cancel_action = Progress.exit)

            return
        else:
            self.explain.SetLabel("Elapsed Time:  %s\n Status: %s" % (status['elapsed'],status['status']))

        self.kill_button.Enable()
        self.Layout()

    def download(self, evt):
        self.wizard.next(Download_Page, project_id=self.project_id)
