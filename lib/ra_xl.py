import logging
import xlwt
import xlrd
import pprint
from lib.utils import *

FunctionType = (lambda(a):a).__class__ # because I can't find a constant for it

class RA_XL(object) :
    # See examplecode/makespreadsheet for usage

    meta_data = [
        ['Meta Info','Do not edit, or import/load may fail.'],
        ['Application','SNS TourSolver','http://www.c2logix.com/toursolverindex.html'],
        ['Format',1],
        ['Type','save'],
        ['Created','Mon, 05 Oct 2009 10:58:41 -0400']
        ]

    xl_format_cache = {} # store easyxf's in here by num_format_str

    def __init__(self,filename) :
        self.filename = filename
        self.book = xlwt.Workbook(encoding="utf-8")
        self.add_meta_sheet()

    @classmethod
    def xl_format(cls, num_format_str) :
        # use the cached format or construct & cache
        # You will get an error if you construct distinct easyxf for each cell
        # after about 4094 of 'em

        if num_format_str not in cls.xl_format_cache :
            cls.xl_format_cache[num_format_str] = xlwt.easyxf(num_format_str = num_format_str)

        return cls.xl_format_cache[num_format_str]

    def write(self) :
        logging.debug("save book as %s" % self.filename)
        self.book.save(self.filename)

    def add_meta_sheet(self):
        sheetname = 'metainfo'
        sheet = self.book.add_sheet(sheetname)   

        s_format = RA_XL.xl_format(num_format_str = '@')
        n_format = RA_XL.xl_format(num_format_str = '0')

        x,y = (0,0)
        for row in self.meta_data:
            y = 0
            for cell in row:
                sheet.write(x, y, cell, n_format if isinstance(cell, int) else s_format)
                y += 1
            x += 1

    class RA_Sheet(object) :
        # class vars: 
        # sheetname
        # header = { RA-Field : "excel format", ... }
        # arc_to_ra_map = { fr-field : ra-field, ... } # for each header field

        def __init__(self, ra_xl) :
            self.field_to_index = {}
            self.did_header = False
            self.sheet = None
            self.row = 0

            # add self to the ra_xl book
            self.sheet = ra_xl.book.add_sheet(self.sheetname)

            # turn header into a mapping of field=>index, and setup the XFStyle object
            i=0
            for h in self.header :
                self.field_to_index[h] = i 
                i+=1

                format_string_or_translate = self.header[h]
                if isinstance(format_string_or_translate, str) :
                    logging.debug( "Header %s is a %s" % (h,format_string_or_translate))
                    format = RA_XL.xl_format(num_format_str = format_string_or_translate)
                    self.header[h] = lambda(v): (format,v)

            logging.debug("%s: fields-to-index %s" % (self.__class__.__name__, inspect(self.field_to_index)))

        def add(self, fleetroute_data_row) :
            # insert one row
            if not self.did_header : self.init_header()

            logging.debug("%s: Write row: %d" % (self.__class__.__name__,self.row))
            for arc_field in fleetroute_data_row :
                if not self.arc_to_ra_map.has_key(arc_field): 
                    # raise LookupError("Your data had a field '"+arc_field+" that has no RA field")
                    continue
                ra_field = self.arc_to_ra_map[arc_field]

                if not self.field_to_index.has_key(ra_field): 
                    raise LookupError("An RA field, '"+ra_field+"', wasnt' mapped to a header column (check the arc_to_ra_map.. vs the ..._header)")
                col = self.field_to_index[ra_field]

                # transform the value
                try:
                    (format, value) = self.header[ra_field](fleetroute_data_row[arc_field])
                except TypeError, e :
                    logging.debug("During value transform of '%s', %s: %s" % (ra_field, fleetroute_data_row[arc_field], e))
                if isinstance(format, str):
                    format = RA_XL.xl_format(num_format_str = format)

                # writes the cell w/the cell-format!
                # logging.debug( "AT '%s' %d,%d, '%s' as %s" % (ra_field,self.row, col, value, format))
                self.sheet.write(self.row, col, value, format)
            self.row += 1

        def init_header(self) :
            logging.debug("%s: Add header %s" % (self.__class__.__name__, inspect(self.header.keys())))
            # write header line
            i=0
            for h in self.header :
                self.sheet.write(0,i,h)
                i+=1
            self.did_header = True
            self.row = 1

    # in ra_xl

    ## transformers should return ( excel_cell_format, newvalue)
    @staticmethod
    def tons_to_pounds(tons) :
        return ('0.00', tons * 2000.0)

    @staticmethod
    def float_to_integer(x) :
        return ('0', int(x))

    @staticmethod
    def convert_to_text(x) :
        return ('@', ("%d"%(x)))
    
    @staticmethod
    def hm_to_miltime(hm) :
        # hm is h:mm
        (h,m) = hm.split(':')
        if len(h) == 1 : h = '0'+h
        return ('@', "%s:%s:00" % (h,m))

    @staticmethod
    def h_to_miltime(in_hours) :
        return RA_XL.to_miltime(in_hours * 60)

    @staticmethod
    def to_miltime(in_minutes) :
        seconds = (in_minutes - int(in_minutes)) * 60
        (hours, minutes) = divmod(in_minutes, 60)
        (days, hours) = divmod(hours, 24)
        if days > 0: raise Exception("Minutes (%d) for conversion to miltime > 1 day" % in_minutes)
        newvalue = "%.2d:%.2d:%.2d" % (hours, minutes,seconds)
        # logger.debug( "to_miltime(%d) -> %s" % (in_minutes,newvalue))
        return ('@', newvalue)
            
class RA_Facility_Sheet(RA_XL.RA_Sheet) :
    sheetname = 'RSS' # 'Depots'
    header = {
        # RA-Field : "excel format"
        "name": RA_XL.convert_to_text,
        "street": '@',
        "longitude": '0.000000',
        "latitude": '0.000000',
        "parameter_fixed_loading_duration": RA_XL.to_miltime,
        }
    arc_to_ra_map = { 
        # fr-field : ra-field 
        "Facil_id": 'name', 
        "Address": 'street',
        "X": 'longitude',
        "Y": 'latitude',
        "XfrWaitTim": 'parameter_fixed_loading_duration',
        }

class RA_Vehicles_Sheet(RA_XL.RA_Sheet) :
    sheetname = 'Vehicles'
    header = {
        # RA-Field : "excel format"
        "name": RA_XL.convert_to_text,
        "facility_id": RA_XL.convert_to_text,
        "longitude": '0.000000',
        "latitude": '0.000000',
        "parameter_vehicle_capacity": RA_XL.tons_to_pounds,
        "parameter_briefing_duration_resource": RA_XL.to_miltime,
        "parameter_debriefing_duration_resource": RA_XL.to_miltime,
        "parameter_start_time" : RA_XL.hm_to_miltime,
        "parameter_time_to_complete" : RA_XL.h_to_miltime,
 
        }
    arc_to_ra_map = { 
        # fr-field : ra-field 
        "Route": 'name',
        "BegFacil": 'facility_id',
        "X": 'longitude',
        "Y": 'latitude',
        "MaxQnty": 'parameter_vehicle_capacity',
        "BegWaitTim": 'parameter_briefing_duration_resource',
        "EndWaitTim": 'parameter_debriefing_duration_resource',
        "Begtime" : 'parameter_start_time',
        "MaxTime" : 'parameter_time_to_complete',
  
        }

class RA_Customers_Sheet(RA_XL.RA_Sheet) :
    sheetname = 'Stops' # 'Customers'
    header = {
        # RA-Field : "excel format"
        "name": RA_XL.convert_to_text,
        "street": '@',
        "parameter_fixed_visit_duration": RA_XL.to_miltime,
        "parameter_unloading_duration_per_unit": RA_XL.float_to_integer,
        "parameter_quantity": RA_XL.float_to_integer,
        "longitude": '0.000000',
        "latitude": '0:000000',
        "parameter_service_side": '0',
        "parameter_time_wdw_1_start": RA_XL.to_miltime,
        "parameter_time_wdw_1_end": RA_XL.to_miltime,
        "parameter_assign_resources": RA_XL.convert_to_text,
        
        }
    arc_to_ra_map = { 
        # fr-field : ra-field 
        "Site_id": 'name',  
        "Site_addr": 'street',  
        "Site_stime": 'parameter_fixed_visit_duration',
        "Site_qnty": 'parameter_quantity',
        "X": 'longitude',
        "Y": 'latitude',
        "Unit_yrd3": 'parameter_unloading_duration_per_unit',
        "Serv_side": 'parameter_service_side',
        "TimeStart": 'parameter_time_wdw_1_start',
        "TimeEnd": 'parameter_time_wdw_1_end',
        "parameter_assign_resources": 'parameter_assign_resources',

        }

class RA_Read_XL(object):
    # FIXME: refactor into RA_XL

    # override these two
    sheetname = 'somesheet name'
    needs_reassembly = None; # column name if there is reassembly

    def __init__(self, filename = None, file = None) :
        # one of: filename or file (an open file)
        self.header_map = {}
        self.headers = []
        self.row_i = 0

        self.filename = filename

        book = xlrd.open_workbook(filename = filename, file_contents = file)
        self.sheet = book.sheet_by_name(self.sheetname)
        self.nrows = self.sheet.nrows
        self.read_header()

    def read_header(self) :
        row = self.sheet.row(0)
        self.row_i += 1
        
        i = 0
        for c in row :
            h_value = c.value
            if h_value == '' or h_value == None: 
                self.headers.append(None)
            else :
                self.header_map[h_value] = i
                self.headers.append(h_value)
            i += 1

    def reassemble_cell(self, row, column_name) :
        # we do a hack for large strings:
        # The cell has the count, the data is at the "end" of the row, for n cells
        i = self.header_map[column_name]
        count = int(row[i].value)
        logging.debug("End data has %d" % count)

        i = len(row) - count
        d = []
        for ii in range(count) :
            d.append( row[i + ii].value )

        return "".join(d)

    def assemble_row(self, row) :
        # returns a dict of the row, doing hack'ish decoding as necessary
        rez = {}
        i = 0
        for c in row :
            h = self.headers[i]
            i += 1
            logging.debug("assemble %s @ %d = %s" % (h,i,inspect(c.value)))
            if h == None: continue
            rez[ h ] = c.value

        if self.needs_reassembly :
            rez[ self.needs_reassembly ] = self.reassemble_cell(row, self.needs_reassembly)

        return rez

    # iterable interface, returns a dict of the xlrd rows
    def __iter__(self) :
        return self

    def next(self) :
        if self.row_i < self.nrows :
            self.row_i += 1
            return self.assemble_row(self.sheet.row(self.row_i - 1))
        else :
            raise StopIteration

class RA_RoutesLineGeometry_Sheet(RA_Read_XL):
    # for reading the RoutesLineGeometry Sheet
    sheetname = 'RoutesLineGeometry'
    needs_reassembly = 'line'

class RA_Routes_Sheet(RA_Read_XL):
    sheetname = 'Route'

