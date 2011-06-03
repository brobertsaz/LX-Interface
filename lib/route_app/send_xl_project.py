#!/usr/bin/env python

import logging
import os
import sys
import urllib2
import urllib
import cookielib
import datetime
import re
from inspect import getmembers

try:
    import json
except ImportError:
    import simplejson as json
from lib.utils import *
from lib.route_app.route_app import Route_App

class Send_XL_Project(Route_App):
    def __init__(self, xl_name, params):
        Route_App.__init__(self)

        self.xl_name = xl_name
        self.errors = None # will have the import errors if it failed
        self.params = params

    def send(self):
        # uploads the xl_name as a project
        # returns:
        #       project_id
        # OR
        #       None, see this.errors for a list of errors

        self.login()

        data = self.json_request('/projects/new.json')
        auth_token = data['authentication_token']

        # upload w/"type"
        logging.debug("\n\n----- Upload")
        rez = None
        ra_params = {
            'authenticity_token' : auth_token,
            'project[name]' : 'FR '+datetime.datetime.today().isoformat(),
            'project[parameter_geocoder_service]' : 'Geocoder::Bing',
            'project[parameter_routing_skips_non_geocoded]' : 'TRUE',
            'project[uploaded_data]' : open(self.xl_name, "rb")
            }

        for k in self.params:
            if re.match('^parameter_', k):
                ra_params['project[%s]' % k] = str(self.params[k]) if self.params[k] != None else ''

        logging.debug("create project with "+inspect(ra_params))

        try:
            rez = self.session.open(self.config['route_app']['base_url'] + '/projects.json', 
                ra_params
                )
        except urllib2.HTTPError, e:
            if e.code >= 200 and e.code < 300:
                # bug in urllib2 before python 2.6
                logging.debug("Caught http result %d %s" % (e.code, e.msg))
                rez = e

            elif e.code == 422:
                # FIXME: only for send:. i.e. make overide method
                data = json.load(e)
                logging.debug("Didn't like our start: "+inspect(data))
                # FIXME: I don't think we actually get errors for this
                self.errors = map(lambda(fe):fe[1],data['errors'])
                return None
            else: 
                logging.debug("Http failed: %d : %s" % (e.code, e.msg))
                raise e
                sys.exit(1)

        logging.debug("Status: %d %s" % (rez.code, rez.msg))
        logging.debug( "Url "+rez.geturl())
        data = json.load(rez)

        logging.debug( "data: "+inspect(data))
        return data['project_id']

