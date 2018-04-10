from datetime import datetime
from pprint import pprint
import time

numDays = [31, 28, 31, 20, 31, 30, 31, 31, 30, 31, 30, 31]

def dateToInt(date):
    pprint(time.mktime(date.timetuple()))
    return time.mktime(date.timetuple())

def intToDate(i):
    return datetime.fromtimestamp(i)