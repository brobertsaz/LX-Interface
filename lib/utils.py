import pprint
import logging

logging.basicConfig(filename='dev.log',level=logging.DEBUG,filemode='w',
    format='%(filename)s::%(funcName)s::%(lineno)d %(levelname)s %(message)s'
    )

_pp = pprint.PrettyPrinter(indent=4)
def inspect(x) :
    return _pp.pformat(x)

def bg_color():
    return'#F2F2F2'

