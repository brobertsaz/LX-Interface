#!/usr/bin/env python

import logging
import os
import sys
import urllib2
import urllib
import re

try:
    import json
except ImportError:
    import simplejson as json
from lib.utils import *
from lib.route_app.route_app import Route_App

class Download(Route_App):
    def __init__(self, project_id):
        Route_App.__init__(self)

        self.project_id = project_id

    def check(self, user):
        # Sanity check
        # returns:
        #       {'error': "...."}
        # OR
        #       {}

        self.login()

        params = { 'parameter[user_data1]': ''}
        data = {}
        try:
            data = self.json_request('/projects/%s/project_info.json' % self.project_id, params = params)
        except urllib2.HTTPError, e:
            if e.code == 404:
                data = { 
                    'user_data1': '{}',
                    'error': "No such project",
                    }
            elif e.code == 422:
                data = { 
                    'user_data1': '{}',
                    'error': json.load(e)['errors']
                    }
            else:
                data = { 
                    'user_data1': '{}',
                    'error': "HTTP failed: %d %s" % (e.code, e.msg)
                    }

        # somebody doesn't collapse \\ correctly.
        user_data = json.loads(data['user_data1'])
        data['user_data1'] = user_data

        if data['error']:
            return data
            logging.debug("data == error")
        else:
            if user != data['user_data1']['user']:
                data['error'] = "Wrong user for that project: %s" % data['user_data1']['user']
                logging.debug("wrong user")
        return data

    def download(self, dir):
        # returns the filename (or crashes)
        dir = re.sub(r'\\\\',r'\\',dir)
        logging.debug("start download "+dir)
        rez = self.session.open(self.config['route_app']['base_url'] + "/projects/%s/save_by_id?wxls=1" % self.project_id)
        logging.debug( "\tfinal url "+rez.geturl())
        # logging.debug( "headers %s" % rez.info().items())
        # logging.debug( "Headers: %s" % inspect(rez.info().headers))

        content_type = rez.info().getheader('content-type')
        if not re.match('^application/octet-stream(;|$)', content_type) : raise Exception("Expected content-type: application/octet-stream, got %s" % content_type)

        disposition = rez.info().getheader('content-disposition')
        fstart = re.search('filename="(.+)',disposition).group(1)
        filename = re.search('^([^"]+)', fstart).group(1)
        filename = re.search('(.+)\.xls$', filename).group(1)
        filename = re.sub('[.:-]','_',filename)
        fullname = os.path.join(dir,filename+".xls")

        logging.debug("opening xl")        
        xl = open(fullname,'wb')

        while 1 :
            block = rez.read(10 * 1024)
            if not block: break
            xl.write(block)
        xl.close()
        logging.debug("ready to return filename")
        return { 'error': None, 'filename': fullname}
