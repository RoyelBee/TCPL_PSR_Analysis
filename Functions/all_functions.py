import pyodbc as db
import datetime
from calendar import monthrange


date = datetime.datetime.now()
current_day = int(date.strftime("%d")) - 1
days_in_month = max(monthrange(int(date.strftime("%Y")), int(date.strftime("%m"))))

conn = db.connect('DRIVER={SQL Server};'
                  'SERVER=10.168.71.36;'
                  'DATABASE=TCPL_SECONDARY;'
                  'UID=ruser;'
                  'PWD=user@123;')


def currency_converter(num):
    num_size = len(str(num))
    if num_size >= 8:
        number = str(round((num / 10000000), 2)) + 'Cr'
    elif num_size >= 7:
        number = str(round(num / 1000000, 2)) + 'M'
    elif num_size >= 4:
        number = str(int(num / 1000)) + 'K'
    else:
        number = num
    return number

def thousand_converter(number):
    number = int(number / 1000)
    number = format(number, ',')
    number = number + 'K'
    return number


def comma_seperator(number):
    number = format(int(number), ',')
    return number

def master_comma_seperator(value):
    if (len(value) > 6):
        return str(value[0:len(value) - 6] + "," + value[len(value) - 6:len(value) - 3] + ","
                   + value[len(value) - 3:len(value)])
    elif (len(value) > 3):
        return str(value[0:len(value) - 3] + "," + value[len(value) - 3:len(value)])
    elif (len(value) > 0):
        return value
    else:
        return "-"
