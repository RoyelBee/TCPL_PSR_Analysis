import datetime
from calendar import monthrange

date = datetime.datetime.now()
current_day = date.strftime("%d")
days_in_month = max(monthrange(int(date.strftime("%Y")), int(date.strftime("%m"))))

num = 60000

cu = []
i = 0
for i in range(days_in_month):
    val = int(num / days_in_month)
    cu.append(val)


def Cumulative(val):
    new = []
    cumsum = 0
    for element in val:
        cumsum += element
        new.append(cumsum)
    return new


cumulativeTarget = Cumulative(cu)


# print(cumulativeTarget[:int(current_day)])


def currency_converter(num):
    num_size = len(str(num))
    if num_size >= 8:
        number = str(round((num / 10000000), 2))+' Cr'
    elif num_size >= 6:
        number = str(round(num / 100000, 2))+' M'
    elif num_size >= 4:
        number = str(round(num / 1000, 2)) +' K'
    else:
        number = num
    return number


print(currency_converter(1135040))
