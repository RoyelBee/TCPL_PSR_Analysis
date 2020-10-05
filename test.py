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
print(cumulativeTarget[:int(current_day)])
