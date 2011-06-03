#!/usr/bin/env python

import wx
from lib.utils import *
import sys, os, glob
import wx.lib.filebrowsebutton
from lib.progress import Progress
import arcgisscripting
from lib.import_stops_from_RW_endpage import Import_Stops_from_RW_endpage


class Import_Stops_from_RW_Page(wx.Panel):

    def __init__(self, wizard, parent ):
        logging.debug("initiating import stops from RW page")
        wx.Panel.__init__(self, parent = parent)

        self.import_stops_picker = None
        self.save_stops_picker = None
        self.parameters_file_picker = None
        self.wizard = wizard
        
        self.SetBackgroundColour(bg_color())

        body_sizer = wx.BoxSizer(orient = wx.VERTICAL)
        self.SetSizer(body_sizer)

        font = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        explain = wx.StaticText(self, -1, 'BLAH')
        explain.SetFont(font)
        body_sizer.Add(explain, flag = wx.EXPAND | wx.ALL, border=5)

        body_sizer.AddSpacer(5)
        body_sizer.Add(wx.StaticLine(self, -1), flag = wx.EXPAND | wx.LEFT | wx.RIGHT, border = 10)
        body_sizer.AddSpacer(5)

        control_sizer = wx.FlexGridSizer(rows=2, cols=2, vgap=5)
        control_sizer.AddGrowableCol(1)
        body_sizer.Add(item = control_sizer, flag = wx.EXPAND | wx.ALL, border = 5)


        control_sizer.Add(item = wx.StaticText(self, -1, ''))
        self.import_stops_picker = wx.lib.filebrowsebutton.FileBrowseButton(self, labelText="Choose the Import file:", 
                fileMask="*.dbf", buttonText='Open')
        control_sizer.Add( item = self.import_stops_picker, flag=wx.EXPAND)

        control_sizer.Add(item = wx.StaticText(self, -1, ''))
        self.save_stops_picker = wx.lib.filebrowsebutton.FileBrowseButton(self, labelText="Save New Customer file as:", 
                fileMask="*.shp", fileMode=2, buttonText='Save')
        control_sizer.Add( item = self.save_stops_picker, flag=wx.EXPAND)
        
        control_sizer.Add(item = wx.StaticText(self, -1, ''))
        self.parameters_file_picker = wx.lib.filebrowsebutton.FileBrowseButton(self, labelText="Select the parameters.dbf:", 
                fileMask="*.dbf", buttonText='Open')
        control_sizer.Add( item = self.parameters_file_picker, flag=wx.EXPAND)


        #self.Bind(wx.EVT_FILEPICKER_CHANGED, self.gotEverything)

        # widgets for tool        

        body_sizer.AddStretchSpacer()

##        back = wx.Button(self, wx.ID_OK, 'Back')
##        back.Bind(wx.EVT_BUTTON, self.onBack)
        next = wx.Button(self, wx.ID_OK, 'Next')
##        next.Disable()
        next.Bind(wx.EVT_BUTTON, self.OnRun) 
        body_sizer.Add(next, flag = wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL, border=10)

##
##    def gotEverything(self,event) :
##        ok_button = self.FindWindowById(wx.ID_OK)
##        if (self.import_stops_picker.GetValue() == '' 
##                or self.save_stops_picker.GetValue() == ''
##                or self.parameters_file_picker.GetValue() == ''
##                ):
##            ok_button.Disable()
##        else :
##            ok_button.Enable()


##    def onBack(self, event):
##        self.wizard.next(Choose_Import_Export)
       
    def OnRun(self, event):
        logging.debug("customer file is: "+self.import_stops_picker.GetValue())        
        logging.debug("ready to open progress")

        self.wizard.next(Progress, message = 'Processing.....')        
        os.chdir(self.wizard.cwd)
        # Create the geoprocessor object
        gp = arcgisscripting.create() 
        Stops = (self.import_stops_picker.GetValue())
        # Set the workspace for the processing files
        gp.workspace = os.path.dirname(Stops)

        # Make copies so that processing doesn't take place on the original.
        gp.Copy_management(Stops, "Stops_process.dbf")


        # Add required fields to Stops

        ## Stops fields that should be carried over
        #gp.AddField_management("Stops_process.dbf", "Site_id", "LONG", 9)
        #gp.AddField_management("Stops_process.dbf", "Site_name", "TEXT", "", "", 30)
        #gp.AddField_management("Stops_process.dbf", "Site_addr", "TEXT", "", "", 65)
        #gp.AddField_management("Stops_process.dbf", "Site_city", "TEXT", "", "", 30)
        #gp.AddField_management("Stops_process.dbf", "Site_state", "TEXT", "", "", 3)
        #gp.AddField_management("Stops_process.dbf", "Site_zip", "TEXT", "", "", 20)
        #gp.AddField_management("Stops_process.dbf", "X", "DOUBLE", 17, 7)
        #gp.AddField_management("Stops_process.dbf", "Y", "DOUBLE", 17, 7)
        #gp.AddField_management("Stops_process.dbf", "Site_units", "LONG", 9)
        #gp.AddField_management("Stops_process.dbf", "Cust_id", "TEXT", "", "", 11)
        #gp.AddField_management("Stops_process.dbf", "Day", "TEXT", "", "", 2)
        #gp.AddField_management("Stops_process.dbf", "Comment", "TEXT", "", "", 254)
        #gp.AddField_management("Stops_process.dbf", "Route", "LONG", 9)


        ## Fields we should get from RFO
        #Serv_code
        #Route_type
        #Time_Window_Start
        #Time_Window_End
        #Setout_rate
        #Serv_side
        #ExportDate


        ## New fields to add
        gp.AddField_management("Stops_process.dbf", "Site_type", "TEXT", "", "", 1)
        gp.AddField_management("Stops_process.dbf", "Serv_type", "TEXT", "", "", 1)
        gp.AddField_management("Stops_process.dbf", "Area", "TEXT", "", "", 15)
        gp.AddField_management("Stops_process.dbf", "Veh_size", "TEXT", "", "", 2)
        gp.AddField_management("Stops_process.dbf", "Unit_stime", "DOUBLE", 11, 4)
        gp.AddField_management("Stops_process.dbf", "Unit_qnty", "DOUBLE", 11, 4)
        gp.AddField_management("Stops_process.dbf", "Site_qnty", "DOUBLE", 11, 4)
        gp.AddField_management("Stops_process.dbf", "Site_stime", "DOUBLE", 11, 4)
        gp.AddField_management("Stops_process.dbf", "Unit_rvnue", "DOUBLE", 11, 2)
        gp.AddField_management("Stops_process.dbf", "Site_rvnue", "DOUBLE", 11, 2)
        gp.AddField_management("Stops_process.dbf", "Unit_yrd3", "DOUBLE", 11, 4)
        gp.AddField_management("Stops_process.dbf", "Cust_name", "TEXT", "", "", 30)
        gp.AddField_management("Stops_process.dbf", "Priority", "LONG", 9)
        gp.AddField_management("Stops_process.dbf", "Requested", "LONG", 9)
        gp.AddField_management("Stops_process.dbf", "Orig_addr", "TEXT", "", "", 65)
        gp.AddField_management("Stops_process.dbf", "Street_id", "LONG", 9)
        gp.AddField_management("Stops_process.dbf", "Av_side", "SHORT", 1)
        gp.AddField_management("Stops_process.dbf", "Av_score", "LONG", 3)
        gp.AddField_management("Stops_process.dbf", "Av_status", "TEXT", "", "", 1)
        gp.AddField_management("Stops_process.dbf", "Corner", "SHORT", 1)
        gp.AddField_management("Stops_process.dbf", "Sameselect", "SHORT", 3)
        gp.AddField_management("Stops_process.dbf", "Sequence", "LONG", 9)
        gp.AddField_management("Stops_process.dbf", "Est_toa", "TEXT", "", "", 8)
        gp.AddField_management("Stops_process.dbf", "Routefile", "TEXT", "", "", 254)
        gp.AddField_management("Stops_process.dbf", "X_route", "LONG", 9)
        gp.AddField_management("Stops_process.dbf", "X_day", "TEXT", "", "", 2)
        gp.AddField_management("Stops_process.dbf", "X_sequence", "LONG", 9)
        gp.AddField_management("Stops_process.dbf", "F_route", "LONG", 9)
        gp.AddField_management("Stops_process.dbf", "F_day", "TEXT", "", "", 2)
        gp.AddField_management("Stops_process.dbf", "F_sequence", "LONG", 9)
        gp.AddField_management("Stops_process.dbf", "F_est_toa", "TEXT", "", "", 8)
        gp.AddField_management("Stops_process.dbf", "F_routefil", "TEXT", "", "", 254)
        gp.AddField_management("Stops_process.dbf", "F_updatecd", "TEXT", "", "", 1)
        gp.AddField_management("Stops_process.dbf", "F_imported", "LONG", 9)
        gp.AddField_management("Stops_process.dbf", "F_exported", "LONG", 9)
        gp.AddField_management("Stops_process.dbf", "F_updated", "LONG", 9)
        gp.AddField_management("Stops_process.dbf", "Up_date", "LONG", 9)
        gp.AddField_management("Stops_process.dbf", "BASE_STIME", "DOUBLE", 11, 4)
        gp.AddField_management("Stops_process.dbf", "XTRSTOPTM", "DOUBLE", 11, 4)
        gp.AddField_management("Stops_process.dbf", "BASE_QNTY", "DOUBLE", 11, 4)
        gp.AddField_management("Stops_process.dbf", "SETOUT_TIM", "DOUBLE", 11, 4)
        gp.AddField_management("Stops_process.dbf", "SETOUT_QNT", "DOUBLE", 11, 4)



        # Make Feature Layer from Stops
        params = (self.parameters_file_picker.GetValue())
        gp.Copy_management(params, "parameterstemp.dbf")
        gp.MakeTableView_management("Stops_process.dbf", "stops")



        # Copy the values from the params table to the stops

        joinTable1 = "stops"
        joinTable2 = "parameterstemp.dbf"
        gp.AddJoin_management(joinTable1, "Serv_code", joinTable2, "Serv_code")
        logging.debug("Joined table views")
        gp.CalculateField_management("stops", "BASE_STIME", "[parameterstemp.BASE_STIME]")
        gp.CalculateField_management("stops", "XTRSTOPTM", "[parameterstemp.XTRSTOPTM]")
        gp.CalculateField_management("stops", "BASE_QNTY", "[parameterstemp.BASE_QNTY]")
        gp.CalculateField_management("stops", "SETOUT_TIM", "[parameterstemp.SETOUT_TIM]")
        gp.CalculateField_management("stops", "SETOUT_QNT", "[parameterstemp.SETOUT_QNT]")
        gp.RemoveJoin_management("stops", "parameterstemp")


        # Calculate fields in the Stops
        logging.debug("Calculating Stops fields...")
        gp.CalculateField_management("stops", "Unit_qnty", "[BASE_QNTY]")
        gp.CalculateField_management("stops", "Unit_stime", "[BASE_STIME]")
        gp.CalculateField_management("stops", "Site_qnty", "[Site_units]*[Unit_qnty]*[SETOUT_QNT]")
        gp.CalculateField_management("stops", "Site_stime", "[Site_units]*[Unit_stime]*[SETOUT_TIM]")


        # Make a point shapefile based on the X,Y in the Stops
        gp.MakeXYEventLayer_management("stops", "X", "Y", "Stops_output")
        gp.CopyFeatures_management("Stops_output", "Stops_output.shp")
        # Create a prj file for Stops_output.shp
        coordsys = "Coordinate Systems/Geographic Coordinate Systems/World/WGS 1984.prj"
        gp.defineprojection("Stops_output.shp", coordsys)


        # Create the output files based on the user's input
        gp.Rename_management("Stops_output.shp", self.save_stops_picker.GetValue())

        # Delete "process" files
        for file in glob.glob(gp.workspace+"/Stops_process*"):    
            os.remove(file)
        for file in glob.glob(gp.workspace+"/parameterstemp*"):    
            os.remove(file)
        for file in glob.glob(gp.workspace+"/*xml"):    
            os.remove(file)

        self.wizard.next(Import_Stops_from_RW_endpage,
                         stops_file = self.save_stops_picker.GetValue()
                         )

     

    








