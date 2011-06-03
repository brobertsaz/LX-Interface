#!/usr/bin/env python

import logging
import sys
try:
    import json
except ImportError:
    import simplejson as json
import datetime
import wx
import urllib2

from lib.utils import *
from lib.route_app.route_app import Route_App

class Route(Route_App):
    Done_Status = [ None, 'terminated', 'error' ]

    def __init__(self, project_id):
        Route_App.__init__(self)

        self.project_id = project_id
        self.errors = None # will have the route errors if it failed

    def start(self, timed = None, stop_when_nearly_done = False):
        # Starts the optimization
        # Supply timed=seconds, or stop_when_nearly_done=True,
        # or it will run till done

        self.login()

        params = {}
        if stop_when_nearly_done: 
            params['route_type'] = 'nearly'
        elif timed:
            params['route_type'] = 'timed'
            params['route_time'] = timed

        try:
            data = self.json_request('/projects/%s/startroute.json' % self.project_id, post = params)
        except urllib2.HTTPError, e:
            if e.code == 404:
                data = {
                    'start' : 0,
                    'error': "No such project",
                    }
            elif e.code == 422:
                # raise Exception(inspect(json.load(e)))
                data = {
                    'start' : 0
##                    'error' : json.load(e)['errors'],
                    }
            else:
                data = {
                    'start' : 0,
                    'error': "HTTP failed: %d %s" % (e.code, e.msg)
                    }

        logging.debug ("start route: "+inspect(data))
        return data

    def monitor(self, observer, seconds, wait_initial = False):
        # observer will get called with the status (same as result of status()), every n seconds
        # You must call cancel_monitor() to stop this,
        # Except, the timer is automatically cancelled if status['running'] is in Done_Status
        # You will get at least one notification, even if it is "not running" (signalled by running=>None)
        # You'll want to set wait_initial=True if you can monitor from your frame's __init__

        current_status = self.status()
        if not wait_initial:
            logging.debug( "Initial monitor status "+inspect(current_status))
            observer(current_status)

        # Don't start if we have None already
        if wait_initial or (not 'running' in current_status or not current_status['running'] in self.Done_Status):
            logging.debug( "Start timer %d" % seconds)
            self.observer = observer
            self.timer = Status_Timer(self)
            self.timer.Start(milliseconds = seconds * 1000)

    def cancel_monitor(self) :
        # Safe to call repeatedly
        logging.debug( "Stop timer")
        if self.timer :
            self.timer.Stop()
            self.observer = None
            self.timer = None

    def update_status(self) :
        # the timer events
        current_status = self.status()

        observer = self.observer

        if current_status['running'] in self.Done_Status:
            logging.debug("Done!")
            self.cancel_monitor()

        observer(current_status)

    def status(self):
        # should return { 'running': ..., 'status':..., 'stopped':... , 'elapsed':...}
        # running and status will be None if there is no optimization
        # See tour_solver/model/optimize_status.rb for the status strings
        # Notably: 
        #       'waiting', 'idle', and 'running' are actually in progress
        #       'undefined' hasn't started at all
        #       'terminated' and 'error' have finished

        self.login()
        
        try:
            data = self.json_request('/projects/%s/query_optimization_status.json' % self.project_id)
        except urllib2.HTTPError, e:
            if e.code == 404:
                data = {
                    'running' : None,
                    'stopped' : None,
                    'status' : "No such project",
                    'elapsed' : None
                    }
            elif e.code == 422:
                # raise Exception(inspect(json.load(e)))
                data = {
                    'running' : None,
                    'stopped' : None,
                    'status' : json.load(e)['errors'],
                    'elapsed' : None
                    }
            else:
                data = {
                    'running' : None,
                    'stopped' : None,
                    'elapsed' : None,
                    'status': "HTTP failed: %d %s" % (e.code, e.msg)
                    }
        return data

    def kill_optimization(self):
        self.login()
    
        try:
            data = self.json_request('/projects/%s/stop_by_id.json' % self.project_id)
        except urllib2.HTTPError, e:
            if e.code == 404:
                data = {
                    'running' : None,
                    'stopped' : None,
                    'status' : "No such project",
                    'elapsed' : None
                    }
            elif e.code == 422:
                # raise Exception(inspect(json.load(e)))
                data = {
                    'running' : None,
                    'stopped' : None,
                    'status' : json.load(e)['errors'],
                    'elapsed' : None
                    }
            else:
                data = {
                    'running' : None,
                    'stopped' : None,
                    'elapsed' : None,
                    'status': "HTTP failed: %d %s" % (e.code, e.msg)
                    }
        logging.debug ("status: "+inspect(data))

class Status_Timer(wx.Timer):
    def __init__(self, monitor):
        wx.Timer.__init__(self)

        self.monitor = monitor
  
    def Notify(self):
        self.monitor.update_status()
