###
# LFUCGStreetImporter.py
# Copyright 2010 C2Logix.  This tool is NOT covered under maintainence for FleetRoute.
# C2Logix is NOT responsible for any changes or modifications made to this tool by the user.
# Unauthorized use of this tool is prohibited.
###

import sys, os, glob
import arcgisscripting

# Create the geoprocessor object   
    
gp = arcgisscripting.create()    


## System arguments
# Input parameters table
table = sys.argv[1]
# Select service type to edit 
servtype = sys.argv[2]
# Stop Time 
basetime = sys.argv[3]
# Site Quantity
baseqnty = sys.argv[4]
# Setout Rate for time
setouttime = sys.argv[5]
# Setout Rate for qnty
setoutqnty = sys.argv[6]
# Extra stop time
xtrastoptime = sys.argv[7]

# Set the workspace for the processing files
gp.workspace = os.path.dirname(sys.argv[1])

gp.AddMessage("Calculating Base Time...")
rows = gp.UpdateCursor(""+table+"")
row = rows.Next()
while row:
    
    # Get the value 
    st = row.GetValue("Serv_code")   
    
    if st == ""+servtype+"":
        # 
        row.BASE_STIME = ""+basetime+""
        row.BASE_QNTY = ""+baseqnty+""
        row.SETOUT_TIM = ""+setouttime+""
        row.SETOUT_QNT = ""+setoutqnty+""       
        row.XTRSTOPTM = ""+xtrastoptime+""
        
    if st != ""+servtype+"":
        # 
        pass
           
    # Execute the new value to the table
    rows.UpdateRow(row)
    # Go to the next
    row = rows.Next()
del rows


# Calculate fields in the Stops
gp.AddMessage("Calculating Parameter fields...")
gp.CalculateField_management(table, "BASE_STIME", "[BASE_STIME]/60")
gp.CalculateField_management(table, "SETOUT_TIM", "[SETOUT_TIM]/100")
gp.CalculateField_management(table, "XTRSTOPTM", "[XTRSTOPTM]/60")
gp.CalculateField_management(table, "SETOUT_QNT", "[SETOUT_QNT]/100")


gp.AddMessage("Process Complete")





