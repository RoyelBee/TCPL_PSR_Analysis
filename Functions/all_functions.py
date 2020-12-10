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