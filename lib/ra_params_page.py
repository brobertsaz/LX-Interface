#!/usr/bin/env python

import wx
import os, sys
import tempfile
from lib.utils import *
from lib import dbf_to_xl
from lib.progress import Progress
from lib.route_app.route import Route
from lib.monitor_optimization_page import Monitor_Optimization_Page
import datetime
import re
try:
    import json
except ImportError:
    import simplejson as json


class RA_Params_Page(wx.Panel):
    
    # Choices for "run-till"
    # wx comboboxes operate in terms of the strings, thus, we end up 
    # Make a constant for the choice (adjust the range):
    Till_Nearly_Done, Till_Done, Till_Time = range(3)
    # Make a string for that choice (just enforce 1:1)
    Run_Till_Choices = (
        # In order, first is the default
        # ( "choice text", constant-from-TILL-above ), ...
        ('Run Until Nearly Done', Till_Nearly_Done),
        ("Run Until It's Done", Till_Done),
        ('Time Limit', Till_Time),
        )

    Sequence_Routes, Create_Routes = range(2)
    # Make a string for that choice:
    Route_Type_Choices = (
        ('Update Sequence Existing Routes', Sequence_Routes),
        ("Create New Routes", Create_Routes),
        )

    def __init__(self, wizard, parent, customer_file, facility_file, vehicle_file):
        logging.debug("initiating")
        wx.Panel.__init__(self, parent = parent)
        
        self.wizard = wizard
        self.customer_file = customer_file
        self.facility_file = facility_file
        self.vehicle_file = vehicle_file
        self.SetBackgroundColour(bg_color())

        body_sizer = wx.BoxSizer(orient = wx.VERTICAL)
        self.SetSizer(body_sizer)

        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        explain = wx.StaticText(self, -1, 'Select the type of routing, the processing times for C2RouteApp and your email \n'
                      +'address for notification when the optimization has been completed. \n'
                      +'\n'
                      +'The optimization my take quite a while and when it is finished you will recieve \n'
                      +'an email notification.')
        
        explain.SetFont(font)
        body_sizer.Add(explain, flag = wx.EXPAND | wx.ALL, border=5)

        body_sizer.AddSpacer(5)
        body_sizer.Add(wx.StaticLine(self, -1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT, border = 10)
        body_sizer.AddSpacer(5)

        control_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=5)
        control_sizer.AddGrowableCol(1)
        body_sizer.Add(item = control_sizer, flag = wx.EXPAND | wx.ALL, border = 5)

        control_sizer.Add(item = wx.StaticText(self, -1, 'Choose the type of routing:  '))
        self.optimization_type = wx.Choice(parent = self, choices = map(lambda(ce): ce[0], self.Route_Type_Choices))
        control_sizer.Add(item = self.optimization_type)

        control_sizer.Add(item = wx.StaticText(self, -1, 'Select process run time:  '))
        self.stop_condition = wx.Choice(parent = self, choices = map(lambda(ce): ce[0], self.Run_Till_Choices))
        control_sizer.Add(item = self.stop_condition)
        self.Bind(wx.EVT_CHOICE, self.toggle_runtime_control, self.stop_condition)
        
        self.maxruntime_text = wx.StaticText(self, -1, 'Enter maximum time to run optimization:')
        control_sizer.Add(item = self.maxruntime_text)
        self.maxruntime = wx.TextCtrl (self, -1, '')
        control_sizer.Add(item = self.maxruntime)

       # default choice disables
        self.maxruntime.Disable()
        self.maxruntime_text.Disable()
        
        control_sizer.Add(item = wx.StaticText(self, -1, 'Enter your email:'))
        self.email = wx.TextCtrl (self, -1, '')
        control_sizer.Add(item = self.email)
       
        body_sizer.AddStretchSpacer()

        finish = wx.Button(self, wx.ID_OK, 'Finish')
        finish.Bind(wx.EVT_BUTTON, self.OnFinish) 
        body_sizer.Add(finish, flag = wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL, border=10)

    def toggle_runtime_control(self, event):
        choice = event.GetSelection()

        if choice == self.Till_Done or choice == self.Till_Nearly_Done :
            self.maxruntime.Disable()
            self.maxruntime_text.Disable()

        if choice == self.Till_Time :
            self.maxruntime.Enable()
            self.maxruntime_text.Enable()


    def OnFinish(self, event):
        if self.maxruntime.IsEnabled() and not re.match('^\d?\d:\d\d:\d\d$', self.maxruntime.GetValue()):
            wx.MessageBox("Invalid format.  Time must be in HH:MM:SS format", 'Error', wx.OK | 
            wx.ICON_ERROR)           
        elif self.email.GetValue() == '':
            wx.MessageBox("Please enter your email address", 'Error', wx.OK | 
            wx.ICON_ERROR)
        else:
            self.start_processing()

        logging.debug("started processing")
        


    def start_processing(self):
        logging.debug("ready to open progress")

        self.wizard.next(Progress, message = 'Processing.....')        
        os.chdir(self.wizard.cwd)

        fh, xl_name = tempfile.mkstemp(suffix=".xls", prefix='project_'+datetime.datetime.today().strftime("%Y%m%d_%H%M%S")+"_", dir=os.path.dirname(self.customer_file))
        os.close(fh)
        os.unlink(xl_name)

        logging.debug("XL: "+xl_name)

        copy_customers_dbf = os.path.splitext(os.path.basename(self.customer_file))[0]+"_results_"+datetime.datetime.today().strftime("%Y%m%d_%H%M%S")+".shp"

        maxruntime = self.maxruntime.GetValue()
        if maxruntime == '' : 
            maxruntime = None
        else:
            h,m,s = maxruntime.split(":")
            maxruntime = ((int(h) * 60) + int(m) * 60) + int(s)

        project_id, errors = dbf_to_xl.process(
            customer_file = self.customer_file,
            facility_file = self.facility_file,
            vehicle_file = self.vehicle_file,
            copy_customers_dbf = copy_customers_dbf,
            save_file = xl_name,
            resequence = self.optimization_type.GetSelection() == self.Sequence_Routes,
            params = {
                'parameter_loading_duration_per_unit' : 0,
                'parameter_notification_email' : self.email.GetValue(),
                'parameter_user_data1' : json.dumps({
                    'dir': os.path.dirname(os.path.abspath(self.customer_file)),
                    'user' : os.environ.get( "USERNAME" ),
                    'copy_customers_dbf' : copy_customers_dbf
                    })
                }
            )

        if project_id:
            self.wizard.next(Progress, message = "Initializing....")
            monitor = Route(project_id)

            args = {}
            stop_condition = self.stop_condition.GetSelection()
            if stop_condition == self.Till_Time :
                args['timed'] = maxruntime
            elif stop_condition == self.Till_Nearly_Done :
                args['stop_when_nearly_done'] = True

            rez = monitor.start(**args)
            if 'start' not in rez:
                wx.MessageBox("There has been an error in routing: "+inspect(rez))
                exit(1)
            logging.debug("ready to open monitor optimization page")

            self.wizard.next(Monitor_Optimization_Page, project_id = project_id)

        else: 
            self.wizard.next(Progress, message = "Failed to send to RouteApp:\n%s" % ",".join(errors))
