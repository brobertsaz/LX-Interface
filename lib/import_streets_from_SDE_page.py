##
# LFUCGStreetImporter.py
# Copyright 2010 C2Logix.  This tool is NOT covered under maintainence for FleetRoute.
# C2Logix is NOT responsible for any changes or modifications made to this tool by the user.
# Unauthorized use of this tool is prohibited.
##

import sys, os, glob

# Create the geoprocessor object
try:
    # 9.2 and beyond    
    import arcgisscripting
    gp = arcgisscripting.create()    
except:    
    # 9.1 and before    
    import win32com.client
    gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")

## System arguments
# Input Streets shapefile
Streets = sys.argv[1]
# Output Streets shapefile 
Streets_output = sys.argv[2]
# Output Streets shapefile 
Streets_output2 = sys.argv[3]
# table for bad streets
Bad_streets = sys.argv[4]
# facility streets layer
facilstr = sys.argv[5]

# Set the workspace for the processing files
gp.workspace = os.path.dirname(sys.argv[4])

# Make copies so that processing doesn't take place on the original.
gp.AddMessage("\nCreating processing files...")
gp.Copy_management(Streets, "Streets_processtemp.shp")
gp.Copy_management(facilstr, "facilstreets.shp")
gp.AddMessage ("Copies created")

# Merge copies of streets to facility streets
strtemp = "Streets_processtemp.shp"
strlist = str(strtemp)+";"+str(facilstr)
outshp = (gp.workspace+"/Streets_processtemp2.shp")
gp.Merge_management (str(strlist), outshp)
gp.AddMessage ("Merged Streets with Facility Streets")

# Change Projection to WGS1984
gp.AddMessage ("Changing Projection to WGS84...")
cs = "C:/Program Files/ArcGIS/Coordinate Systems/Geographic Coordinate Systems/World/WGS 1984.prj"
gp.Project ("Streets_processtemp2.shp", "Streets_process.shp", cs, "NAD_1983_To_WGS_1984_1")


# Add required fields to Streets
gp.AddMessage("Adding fields to Streets...")

gp.AddField_management("Streets_process.shp", "Street_id", "LONG", 9)
gp.AddField_management("Streets_process.shp", "Src_str_id", "LONG", 9)
gp.AddField_management("Streets_process.shp", "L_f_add", "TEXT","","", 5)
gp.AddField_management("Streets_process.shp", "L_t_add", "TEXT","","", 5)
gp.AddField_management("Streets_process.shp", "R_f_add", "TEXT","","", 5)
gp.AddField_management("Streets_process.shp", "R_t_add", "TEXT","","", 5)
gp.AddField_management("Streets_process.shp", "Prefix", "TEXT","","", 1)
#gp.AddField_management("Streets_process.shp", "Name", "TEXT","","", 25)
gp.AddField_management("Streets_process.shp", "Type", "TEXT","","", 4)
gp.AddField_management("Streets_process.shp", "Suffix", "TEXT","","", 1)
gp.AddField_management("Streets_process.shp", "ZipL", "TEXT","","", 5)
gp.AddField_management("Streets_process.shp", "ZipR", "TEXT","","", 5)
gp.AddField_management("Streets_process.shp", "Full_name", "TEXT","","", 35)
gp.AddField_management("Streets_process.shp", "Class", "SHORT", 3)
gp.AddField_management("Streets_process.shp", "FRSpeed", "SHORT", 3)
gp.AddField_management("Streets_process.shp", "Drivingtim", "DOUBLE", 11, 4)
gp.AddField_management("Streets_process.shp", "WalkingTim", "DOUBLE", 11, 4)
gp.AddField_management("Streets_process.shp", "One_way", "TEXT","","", 4)
gp.AddField_management("Streets_process.shp", "Extra_pass", "SHORT", 3)
gp.AddField_management("Streets_process.shp", "Veh_size", "TEXT","","", 2)
gp.AddField_management("Streets_process.shp", "Lcusts", "SHORT", 4)
gp.AddField_management("Streets_process.shp", "Rcusts", "SHORT", 4)
gp.AddField_management("Streets_process.shp", "Bcusts", "SHORT", 4)
gp.AddField_management("Streets_process.shp", "Lunits", "SHORT", 4)
gp.AddField_management("Streets_process.shp", "Runits", "SHORT", 4)
gp.AddField_management("Streets_process.shp", "Bunits", "SHORT", 4)
gp.AddField_management("Streets_process.shp", "Lservetime", "DOUBLE", 11, 4)
gp.AddField_management("Streets_process.shp", "Rservetime", "DOUBLE", 11, 4)
gp.AddField_management("Streets_process.shp", "Bservetime", "DOUBLE", 11, 4)
gp.AddField_management("Streets_process.shp", "Lquantity", "DOUBLE", 11, 4)
gp.AddField_management("Streets_process.shp", "Rquantity", "DOUBLE", 11, 4)
gp.AddField_management("Streets_process.shp", "Bquantity", "DOUBLE", 11, 4)
gp.AddField_management("Streets_process.shp", "Lrevenue", "DOUBLE", 11, 2)
gp.AddField_management("Streets_process.shp", "Rrevenue", "DOUBLE", 11, 2)
gp.AddField_management("Streets_process.shp", "Brevenue", "DOUBLE", 11, 2)
gp.AddField_management("Streets_process.shp", "Lroute", "LONG", 9)
gp.AddField_management("Streets_process.shp", "Rroute", "LONG", 9)
gp.AddField_management("Streets_process.shp", "Broute", "LONG", 9)
gp.AddField_management("Streets_process.shp", "LRoutefile", "TEXT","","", 254)
gp.AddField_management("Streets_process.shp", "RRoutefile", "TEXT","","", 254)
gp.AddField_management("Streets_process.shp", "LPriority", "LONG", 9)
gp.AddField_management("Streets_process.shp", "RPriority", "LONG", 9)
gp.AddField_management("Streets_process.shp", "LSP", "LONG", 9)
gp.AddField_management("Streets_process.shp", "RSP", "LONG", 9)
gp.AddField_management("Streets_process.shp", "LCycle", "LONG", 9)
gp.AddField_management("Streets_process.shp", "RCycle", "LONG", 9)
gp.AddField_management("Streets_process.shp", "CycleLegnd", "LONG", 9)
gp.AddField_management("Streets_process.shp", "To_Z", "SHORT", 3)
gp.AddField_management("Streets_process.shp", "From_Z", "SHORT", 3)
#gp.AddField_management("Streets_process.shp", "Length", "DOUBLE", 11, 4)
gp.AddField_management("Streets_process.shp", "Width", "SHORT", 3)
gp.AddField_management("Streets_process.shp", "Lfacil", "LONG", 9)
gp.AddField_management("Streets_process.shp", "Rfacil", "LONG", 9)
gp.AddField_management("Streets_process.shp", "Lfacilcost", "DOUBLE", 11, 4)
gp.AddField_management("Streets_process.shp", "Rfacilcost", "DOUBLE", 11, 4)
gp.AddField_management("Streets_process.shp", "X_LRoute", "LONG", 9)
gp.AddField_management("Streets_process.shp", "X_RRoute", "LONG", 9)
gp.AddField_management("Streets_process.shp", "X_BRoute", "LONG", 9)
gp.AddField_management("Streets_process.shp", "Sameselect", "SHORT", 3)
gp.AddField_management("Streets_process.shp", "Neterr", "TEXT","","", 10)
gp.AddField_management("Streets_process.shp", "Neterr_ok", "TEXT","","", 10)
gp.AddField_management("Streets_process.shp", "Neterr_id", "LONG", 9)
gp.AddField_management("Streets_process.shp", "Up_date", "DATE", 9)
gp.AddField_management("Streets_process.shp", "Serv_mode", "TEXT","","", 1)
gp.AddField_management("Streets_process.shp", "Serv_area", "TEXT","","", 3)
gp.AddField_management("Streets_process.shp", "LComment", "TEXT","","", 50)
gp.AddField_management("Streets_process.shp", "RComment", "TEXT","","", 50)

gp.AddMessage("Making Layers & Views...")
# Make Feature Layer from Streets
gp.MakeFeatureLayer("Streets_process.shp", "Streets")
gp.Copy_management (Bad_streets, "excludetemp.dbf")

# Calculate the Serv_area in the Streets
gp.AddMessage("Calculate Serv_area from excludestreets.dbf to Streets...")
joinTable = "excludetemp.dbf"
gp.AddJoin_management("Streets", "SCLINK", joinTable, "SCLINK")
gp.CalculateField_management("Streets", "Serv_area", "[excludetemp.Serv_area]")
gp.RemoveJoin_management("Streets", "excludetemp") 



# Create update cursor for feature class to update the Class field and change the zero to nine.
rows = gp.UpdateCursor("Streets")
row = rows.Next()
while row:
    
    # Get the value for each record in field ClassCode and assign it to variable "cc"
    cc = row.GetValue("RDCLASS")   
    
    if cc == 0:
        # Put the number 9 in field Class
        row.Class = 9
    if cc > 0 and cc < 10:
        # Put the value of field ClassCode in field Class
        row.Class = cc
    if cc > 10:
        # Put the value of field ClassCode in field Class
        row.Class = 9
           
    # Execute the new value to the table
    rows.UpdateRow(row)
    # Go to the next
    row = rows.Next()
del rows

# Create update cursor for feature class to create the correct one way field formatting.
rows = gp.UpdateCursor("Streets")
row = rows.Next()
while row:
    
    # Get the value for each record in field ClassCode and assign it to variable "oneway"
    oneway = row.GetValue("ONEWAY")   
    
    if oneway == "FT":
        # Put the value FT in field One_way
        row.One_way = "FT"
    if oneway == "TF":
        # Put the value TF in field One_way
        row.One_way = "TF"
    if oneway == "B":
        # Put the value FT in field One_way
        row.One_way = ""
           
    # Execute the new value to the table
    rows.UpdateRow(row)
    # Go to the next
    row = rows.Next()
del rows

# Create update cursor for feature class to calculate the speed of zero.
rows = gp.UpdateCursor("Streets")
row = rows.Next()
while row:    

    # Get the value for each record in field Class and assign it to variable "Speed"
    spd = row.GetValue("SPEED")       

    if spd == 0:
        # Put the number 15 in field Speed
        row.FRSpeed = 15
    if spd > 0:
        # Put the value of field ClassCode in field Speed
        row.FRSpeed = spd      

    # Execute the new value to the table
    rows.UpdateRow(row)
    # Go to the next
    row = rows.Next()
del rows

# Calculate fields in the Streets
gp.AddMessage("Calculating Street fields...")
gp.CalculateField_management("Streets", "Street_id", "[SCLINK]")
gp.CalculateField_management("Streets", "SPEED", "[FRSpeed]")
gp.CalculateField_management("Streets", "L_f_add", "[LFROM]")
gp.CalculateField_management("Streets", "L_t_add", "[LTO]")
gp.CalculateField_management("Streets", "R_f_add", "[RFROM]")
gp.CalculateField_management("Streets", "R_t_add", "[RTO]")
gp.CalculateField_management("Streets", "Full_name", "[ROADNAME]")
gp.CalculateField_management("Streets", "Type", "[TYPE]")
gp.CalculateField_management("Streets", "ZipL", "[ZIP_LEFT]")
gp.CalculateField_management("Streets", "ZipR", "[ZIP_RIGHT]")
gp.CalculateField_management("Streets", "Length", "[SHAPE_len]")
gp.CalculateField_management("Streets", "Up_Date", "[UPDATE_]")
gp.CalculateField_management("Streets", "Drivingtim", "[Length]/[SPEED]/5280*60")



# Create copies for the 2 different streets
gp.AddMessage("Creating the Street Outputs file...")
gp.CopyFeatures("Streets", "Streets_output.shp")
gp.CopyFeatures("Streets", "Streets_output2.shp")

# Calculate the extra_pass field different for the Herbie/Rosie and the Lennys
gp.AddMessage("Calculating the Extra Pass fields...")
# Create update Cursor for the Herbie/Rosie streets
# All non one ways are extra pass = 1
rows = gp.UpdateCursor("Streets_Output.shp")
row = rows.Next()
while row:    

    # Get the value for each record in field One way
    oneway = row.GetValue("One_way")       

    if oneway == " ":
        # Put the number 1 in field Extra_pass
        row.Extra_pass = 1
         

    # Execute the new value to the table
    rows.UpdateRow(row)
    # Go to the next
    row = rows.Next()
del rows

# Create update Cursor for the Lenny streets
# All non one ways are extra pass = 1
rows = gp.UpdateCursor("Streets_Output2.shp")
row = rows.Next()
while row:    

    # Get the value for each record in field SPEED
    oneway = row.GetValue("One_way")
    spd = row.GetValue ("SPEED")

    if oneway == " " and spd > 25:
        # Put the number 1 in field Extra_pass
        row.Extra_pass = 1
         

    # Execute the new value to the table
    rows.UpdateRow(row)
    # Go to the next
    row = rows.Next()
del rows



# Create the output files based on the user's input
gp.AddMessage("Creating final output files...")
gp.Rename_management("Streets_output.shp", Streets_output)
gp.Rename_management("Streets_output2.shp", Streets_output2)


gp.AddMessage("Cleanup...")
# Delete "process" files

for file in glob.glob(gp.workspace+"/Streets_process*"):    
    os.remove(file)
for file in glob.glob(gp.workspace+"/Streets_output*"):    
    os.remove(file)
for file in glob.glob(gp.workspace+"/facilstreets*"):
    os.remove(file)
for file in glob.glob(gp.workspace+"/excludetemp*"):
    os.remove(file)
for file in glob.glob(gp.workspace+"/*.xml"):    
    os.remove(file) 
gp.AddMessage("\nDone.\n")
