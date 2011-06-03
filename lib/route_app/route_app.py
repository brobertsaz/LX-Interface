import logging
import sys, os
import urllib, urllib2, cookielib
try:
    import json
except ImportError:
    import simplejson as json
import datetime
import re

from lib import MultipartPostHandler
from lib.utils import *

class Route_App(object):

    def __init__(self):
        self.session = None # an "opener", aka user-agent
        self._logged_in = False
        if os.environ.get('ITOOL_CONFIG'):
            logging.debug("Using Config "+os.environ.get('ITOOL_CONFIG'))
        config_file = os.environ.get('ITOOL_CONFIG') or "config.json"
        self.config = json.load(open(os.path.join("config",config_file)))

        # setup for cookie-preservation:
        cookie_jar = cookielib.CookieJar()

        self.session = urllib2.build_opener( urllib2.HTTPCookieProcessor(cookie_jar), MultipartPostHandler.MultipartPostHandler )
        urllib2.install_opener( self.session )

    def login(self, force = False):
        if not force and self._logged_in :
            logging.debug("Already logged in")
            return

        # login (keep "session")

        data = self.json_request('/session.json', post = { 'login': self.config['route_app']['username'], 'password': self.config['route_app']['password'] })
        if not data['logged_in'] :
            raise Exception("Didn't log in!")
        self._logged_in = True

    def json_request(self, path, params = None, post = None) :
        if params:
            logging.debug( "jsonreq "+inspect(params))
            path += "?"+urllib.urlencode(params) 
        elif post:
            post = json.dumps(post)
        logging.debug( "%s %s w/%s" % (("POST" if post else "GET"), path, inspect(post)))

        req = urllib2.Request(
            self.config['route_app']['base_url'] + path,
            post,
            {'Content-Type': 'application/json'} # must use the header for json
            )
        # see HTTPMessage
        rez = self.session.open(req)
        logging.debug( "\tfinal url "+rez.geturl())
        # logging.debug( "headers %s" % rez.info().items())
        logging.debug( "json data %s bytes" % (rez.info().getheader('content-length')))
        # logging.debug( "Headers: %s" % inspect(rez.info().headers))

        content_type = rez.info().getheader('content-type')
        if not re.match('^application/json(;|$)', content_type) : raise Exception("Expected content-type: application/json, got %s" % content_type)

        data = json.load(rez) if rez.info().getheader('content-length') else None
        logging.debug( "data: "+inspect(data))
        return data
        
