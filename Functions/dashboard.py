from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import pyodbc as db
from datetime import datetime
import datetime as dd
import pytz

# # --------- Import local files -----------------
import Functions.kpi as kpi

date = datetime.today()
day = str(date.day) + '/' + str(date.month) + '/' + str(date.year)
tz_NY = pytz.timezone('Asia/Dhaka')
datetime_BD = datetime.now(tz_NY)
time = datetime_BD.strftime("%I:%M %p")
date = datetime.today()
x = dd.datetime.now()
day = str(date.day) + '-' + str(x.strftime("%b")) + '-' + str(date.year)
# print(date)
print(day)
tz_NY = pytz.timezone('Asia/Dhaka')
datetime_BD = datetime.now(tz_NY)
time = datetime_BD.strftime("%I:%M %p")
print(datetime_BD)
print(time)
img = Image.open("../Images/dash_structure.png")
title = ImageDraw.Draw(img)
timestore = ImageDraw.Draw(img)
name = ImageDraw.Draw(img)
desig = ImageDraw.Draw(img)
boss = ImageDraw.Draw(img)
dateL = ImageDraw.Draw(img)
timeL = ImageDraw.Draw(img)
targetL = ImageDraw.Draw(img)
salesL = ImageDraw.Draw(img)
achivL = ImageDraw.Draw(img)
returnL = ImageDraw.Draw(img)


# # ------- Weight Pointer ----------------------
wTargetL = ImageDraw.Draw(img)
wSalesL = ImageDraw.Draw(img)
achivL = ImageDraw.Draw(img)
returnL = ImageDraw.Draw(img)

# # ---------------------------------------------

Stencil_Regular = ImageFont.truetype("../font_styles/Lobster-Regular.ttf", 60, encoding="unic")
Viga = ImageFont.truetype("../font_styles/Viga-Regular.ttf", 30, encoding="unic")

Name = kpi.sr_name
designation = kpi.designation
reporting_boss = kpi.reporting_boss

# # ------------ Profile section ---------------------------------
name.text((66, 15), Name , (255, 255, 255), font=Stencil_Regular)
desig.text((66, 100), designation , (255, 255, 255), font=Viga)
boss.text((280, 165), reporting_boss , (255, 255, 255), font=Viga)
dateL.text((1050, 50), str(day) , (29, 34, 105), font=Viga)
timeL.text((1050, 137), str(time) , (29, 34, 105), font=Viga)

# # ------ Value Section  ----------------------------------------
target = kpi.currency_converter(kpi.total_val_target)
sales = kpi.currency_converter(kpi.sales_val)
achiv = round((kpi.sales_val/kpi.total_val_target)*100, 2)

targetL.text((70, 400),  str(target) , (255, 255, 255), font=Viga)
salesL.text((330, 400),  str(sales) , (255, 255, 255), font=Viga)
achivL.text((600, 400),  str(achiv) +"%", (255, 255, 255), font=Viga)


val_return_p = round((kpi.total_val_return/kpi.sales_val)*100, 2)
returnL.text((1100, 550),  str(val_return_p) +"%", (255, 255, 255), font=Viga)



# # --------- Weight wise KPI -------------------------------------------
Wtarget = kpi.currency_converter(kpi.total_weight_target)
WSalesKg = kpi.currency_converter(kpi.sales_kg)
achivKg = round((kpi.sales_kg/kpi.total_weight_target)*100, 2)
kg_return_p = round((kpi.total_weight_return/kpi.sales_kg)*100, 2)


wTargetL.text((70, 810),  Wtarget, (255, 255, 255), font=Viga)
wSalesL.text((340, 810),  WSalesKg, (255, 255, 255), font=Viga)
achivL.text((600, 810),  str(achivKg) +"%", (255, 255, 255), font=Viga)
returnL.text((1100, 960),  str(kg_return_p) +"%", (255, 255, 255), font=Viga)



img.save('../Images/dashboard.png')