import os, glob
import arcgisscripting
from . import ra_xl
from lib.utils import *
from lib.route_app.send_xl_project import Send_XL_Project

def process( facility_file, vehicle_file, customer_file, save_file, copy_customers_dbf, resequence, params) :
    gp = arcgisscripting.create(9.3)
    # Set the workspace and table views of the originals
    gp.workspace = os.path.dirname(save_file)

    for file in glob.glob(gp.workspace+"/facilitytemp*"):    
        os.remove(file)
    for file in glob.glob(gp.workspace+"/vehicletemp*"):    
        os.remove(file)
    for file in glob.glob(gp.workspace+"/customertemp*"):
        os.remove(file)
    for file in glob.glob(gp.workspace+"/Original_Customers*"):
        os.remove(file)
    for file in glob.glob(gp.workspace+"/*.xml"):    
        os.remove(file)

    gp.maketableview(facility_file, "facility")
    gp.maketableview(vehicle_file, "vehicle")
    gp.maketableview(customer_file, "customer")

    gp.Copy_management(customer_file, copy_customers_dbf)

    # make new tables from the views
    gp.copyrows("facility", "facilitytemp.dbf")
    gp.copyrows("vehicle", "vehicletemp.dbf")
    gp.copyrows("customer", "customertemp.dbf")

    ## Begin exporting to xls
    ##
    ##
    ra_book = ra_xl.RA_XL(save_file) # don't forget to include the directory in the path!)

    
    ## Vehicles sheet
    vehicles = ra_xl.RA_Vehicles_Sheet(ra_book)

    # get the fields that are in the table
    fields = map(lambda(f): f.Name, gp.ListFields("vehicletemp.dbf"))
        
    c = gp.SearchCursor("vehicletemp.dbf")

    row = c.Next()
    first_XfrWaitTim = row.GetValue('XfrWaitTim') # need for depot
    while row:
        if row.Begtime == '' or row.Begtime == None :
            row = c.Next()
            continue # skip unrouted rows

        data = dict((f, row.GetValue(f)) for f in fields)
        vehicles.add(data)
        row = c.Next()

    # DEPOT sheet
    depots = ra_xl.RA_Facility_Sheet(ra_book)

    # get the fields that are in the table
    fields = map(lambda(f): f.Name, gp.ListFields("facilitytemp.dbf"))
        
    c = gp.SearchCursor("facilitytemp.dbf")

    row = c.Next()
    while row:
        data = dict((f, row.GetValue(f)) for f in fields)
        data['XfrWaitTim'] = first_XfrWaitTim
        depots.add(data)
        row = c.Next()

    # customers sheet
    customers = ra_xl.RA_Customers_Sheet(ra_book)

    # get the fields that are in the table
    fields = map(lambda(f): f.Name, gp.ListFields("customertemp.dbf"))
    logging.debug("customer fields "+ inspect(fields))

    c = gp.SearchCursor("customertemp.dbf")

    row = c.Next()
    while row:
        data = dict((f, row.GetValue(f)) for f in fields)

        if resequence: 
            logging.debug("Making customer row for %s with Route %s" %(row.Site_id, inspect(row.Route)))
            if row.Route == 0: 
                row = c.Next()
                continue # skip unrouted rows
            data['parameter_assign_resources'] = row.Route
        customers.add(data)
        logging.debug("customer data "+ inspect(data))
        row = c.Next()

    # DONE
    ra_book.write()
    logging.debug("just about to send")
    sender = Send_XL_Project(save_file, params = params)
    project_id = sender.send()
    if project_id : logging.debug("Project id =%s" % project_id)
    logging.debug("errors %s" % inspect(sender.errors))

    # Clean up the temp files
    for file in glob.glob(gp.workspace+"/facilitytemp*"):    
        os.remove(file)
    for file in glob.glob(gp.workspace+"/vehicletemp*"):    
        os.remove(file)
    for file in glob.glob(gp.workspace+"/customertemp*"):
        os.remove(file)
    for file in glob.glob(gp.workspace+"/facility_process*"):    
        os.remove(file)
    for file in glob.glob(gp.workspace+"/vehicle_process*"):    
        os.remove(file)
    for file in glob.glob(gp.workspace+"/customer_process*"):
        os.remove(file)
    for file in glob.glob(gp.workspace+"/*.xml"):    
        os.remove(file)
    
    return (project_id, None if project_id else sender.errors)
