# Create the Geoprocessor object
gp = arcgisscripting.create()
def row_is_valid(row_num, row):
    is_valid = True
    if row.GetValue("Cust_id") == None or row.GetValue("Cust_id") == 0 or row.GetValue("Cust_id") == '' or row.GetValue("Cust_id") == ' ':
        is_valid = False
        gp.AddMessage("Invalid: Row %d Cust_id is blank" % row_num)
    return is_valid
    if row.GetValue("X") == None or row.GetValue("X") == 0 or row.GetValue("X") == '' or row.GetValue("X") == ' ':
        is_valid = False
        gp.AddMessage("Invalid: Row %d Longitude is blank or incorrect" % row_num)
    return is_valid
    if row.GetValue("Y") == None or row.GetValue("Y") == 0 or row.GetValue("Y") == '' or row.GetValue("Y") == ' ':
        is_valid = False
        gp.AddMessage("Invalid: Row %d Latitude is blank or incorrect" % row_num)
    return is_valid
    if row.GetValue("Route") == None or row.GetValue("Route") == 0 or row.GetValue("Route") == '' or row.GetValue("Route") == ' ':
        is_valid = False
        gp.AddMessage("Invalid: Row %d Route is blank or invalid" % row_num)
    return is_valid
    if row.GetValue("Sequence") == None or row.GetValue("Sequence") == 0 or row.GetValue("Sequence") == '' or row.GetValue("Sequence") == ' ':
        is_valid = False
        gp.AddMessage("Invalid: Row %d Sequence is blank or invalid" % row_num)
    return is_valid
    if row.GetValue("Day") == None or row.GetValue("Day") == 0 or row.GetValue("Day") == '' or row.GetValue("Day") == ' ':
        is_valid = False
        gp.AddMessage("Invalid: Row %d Day is blank or invalid" % row_num)
    return is_valid




 

gp.AddMessage("Starting Update Cursor")

cursor=gp.UpdateCursor(stops_in, query)

row=cursor.Next()

while row <> None:
    row.ExportDate = datetime.today().isoformat()
    cursor.UpdateRow(row)
    row = cursor.Next()

del cursor   


output=open(stops_output,'w')
linewriter=csv.writer(output,delimiter='|')


good_fields = ['Site_name', 'Cust_id', 'X', 'Y', 'Serv_code', 'Route_type', 'Route', 'Sequence', 'Serv_side', 'Day', 'Est_toa', 'ExportDate']

gp.AddMessage("Listed fields")

flds=gp.ListFields(stops_in)
fld = flds.Next()
header=[]
while fld:
    if fld.Name in good_fields: 
        value=fld.Name
        header.append(value)
    fld = flds.Next()
linewriter.writerow(header)


gp.AddMessage("Starting search cursor")

gp.AddMessage("Query is "+query)

cursor=gp.SearchCursor(stops_in, query)

row=cursor.Next()

row_num = 1
while row:
    line=[]
    if row_is_valid(row_num, row):
        for fld in header:
            value=row.GetValue(fld)
            line.append(value)
        linewriter.writerow(line)
    row=cursor.Next()
    row_num += 1
    
del cursor

gp.AddMessage("Finished")

output.close()