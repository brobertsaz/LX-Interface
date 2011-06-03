#!/usr/bin/env python

#import wxversion
#wxversion.ensureMinimal('2.6')
import wx
import os 
import sys
from wx.lib.wordwrap import wordwrap
from lib.utils import *
from lib.progress import Progress
from lib.start_page import Start_Page
from lib.help_text import help_text

class Choose_Import_Export(wx.Frame):

    def __init__(self, title, cwd, start = Start_Page, start_args = {}):

        self.cwd = cwd
        self.body_panel = None
        self.top_panel = None

        wx.Frame.__init__(self, parent=None, title=title, pos=(150,150))
        
        panel = wx.Panel(self, -1)
        self.top_panel = panel
        panel.SetBackgroundColour(bg_color())

        ## Menu Bar and functions
        menuBar=wx.MenuBar()        
        menu1=wx.Menu()
        menu1.Append(101, "&Help", "Help using this tool")
        menu1.Append(102, "&About", "About this Tool")
        menuBar.Append(menu1, "&Help")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.show_help, id=101)
        self.Bind(wx.EVT_MENU, self.Menu102, id=102)

        topsizer = wx.BoxSizer(orient = wx.VERTICAL)
        self.topsizer = topsizer
        panel.SetSizer(topsizer)

        bmp = wx.Bitmap(name = 'images/FR-C2RA-header.png', type = wx.BITMAP_TYPE_PNG)
        topsizer.Add(
            item = wx.StaticBitmap(parent=panel, bitmap=bmp),
            flag = wx.ALIGN_CENTER)

        self.next(start, **start_args)

    def show_help(self, event):
        wx.MessageBox(help_text[self.body_panel.__class__.__name__])

    def Menu102(self, event):
        # First we create and fill the info object
        info = wx.AboutDialogInfo()
        info.Name = "FleetRoute to C2RouteApp Importer"
        info.Version = "1.0"
        info.Copyright = "(C) 2010 C2Logix"
        info.Description = wordwrap(
            "The \"FleetRoute - C2RouteApp Interface\" tool is a software program created by C2Logix that can be used "
            "for transferring files from FleetRoute to the C2RouteApp for routing using the point-to-point"
            " algorithm, and to download the resulting route files.",
            350, wx.ClientDC(self))
        info.WebSite = ("http://www.C2Logix.com", "C2Logix Home Page")
        info.Developers = [ "Bob Roberts",
                            "Alan Grover",]

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)
       
    def next(self, cls, **kwargs):
        # passes through extra keyword args to the "page" constructor
        if self.body_panel:
            self.body_panel.Hide()
            self.topsizer.Remove(self.body_panel)
            # don't destroy the page, so its event handlers can do stuff after doing a Progress.

        new = cls(wizard = self, parent = self.top_panel, **kwargs)

        self.body_panel = new
        self.topsizer.Add(item = new, flag = wx.EXPAND)
        self.topsizer.SetSizeHints( self.top_panel )
        self.topsizer.Fit(self)
        self.top_panel.Layout()
     
    @staticmethod
    def exit(x):
        # useful for cancel_action in Progress
        logging.debug("Exit called")
        sys.exit(1)


logging.debug("Start")
os.chdir(os.path.dirname( os.path.abspath(sys.argv[0])))

more_args = {}

if len(sys.argv) > 1:
    import imp

    del sys.argv[0]

    page_class = sys.argv[0]
    del sys.argv[0]

    new_mod = imp.load_source("lib."+page_class.lower(),"lib/"+page_class.lower()+".py")

    print "loaded %s" % new_mod
    more_args['start'] = getattr(new_mod, page_class)
    more_args['start_args'] = dict( [ (sys.argv[i], sys.argv[i+1]) for i in range(0,len(sys.argv),2)]) if len(sys.argv) > 0 else {}


try:
    app = wx.App()   # Error messages go to popup window
    top = Choose_Import_Export(title = "FleetRoute / C2RouteApp Interface Tool", cwd = os.getcwd(), **more_args)
    top.Show()
    app.MainLoop()
finally:
    del app
logging.debug("Ran off end")
