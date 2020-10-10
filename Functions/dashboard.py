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
trendVal = ImageDraw.Draw(img)
trendPer = ImageDraw.Draw(img)
drop_size_val = ImageDraw.Draw(img)


# # ------- Weight Pointer ----------------------
wTargetL = ImageDraw.Draw(img)
wSalesL = ImageDraw.Draw(img)
achivL = ImageDraw.Draw(img)
returnL = ImageDraw.Draw(img)
trendW = ImageDraw.Draw(img)
trendValW = ImageDraw.Draw(img)
drop_sizeW = ImageDraw.Draw(img)

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
mtd_target = int((kpi.total_val_target/kpi.days_in_month)* kpi.current_day)
target = kpi.currency_converter(mtd_target)
sales = kpi.currency_converter(kpi.sales_val)
achiv = round((kpi.sales_val/mtd_target)*100, 2)
trendval = kpi.currency_converter(int(kpi.trend_val))

targetL.text((70, 400),  str(target) , (255, 255, 255), font=Viga)
salesL.text((330, 400),  str(sales) , (255, 255, 255), font=Viga)
achivL.text((600, 400),  str(achiv) +"%", (255, 255, 255), font=Viga)
trendVal.text((850, 400),  str(trendval) , (255, 255, 255), font=Viga)
trendPer.text((1100, 400),  str(kpi.trend_percent) + "%"  , (255, 255, 255), font=Viga)


val_return_p = round((kpi.total_val_return/kpi.sales_val)*100, 2)
drop_size_val.text((850, 550), str(kpi.currency_converter(kpi.val_drop_size)) , (255, 255, 255), font=Viga)
returnL.text((1100, 550),  str(val_return_p) +"%", (255, 255, 255), font=Viga)



# # --------- Weight wise KPI -------------------------------------------
mtd_weight_target = int((kpi.total_weight_target/kpi.days_in_month)* kpi.current_day)
WSalesKg = kpi.sales_kg
achivKg = round((kpi.sales_kg/mtd_weight_target)*100, 2)
kg_return_p = round((kpi.total_weight_return/kpi.sales_kg)*100, 2)


wTargetL.text((70, 810),  str(mtd_weight_target) + ' Kg', (255, 255, 255), font=Viga)
wSalesL.text((340, 810),  str(WSalesKg) + ' Kg', (255, 255, 255), font=Viga)
achivL.text((600, 810),  str(achivKg) +"%", (255, 255, 255), font=Viga)
trendW.text((840, 810),  str(int(kpi.trend_val_kg)) + ' Kg', (255, 255, 255), font=Viga)
trendValW.text((1100, 810),  str(kpi.w_trend_per) + "%"  , (255, 255, 255), font=Viga)


returnL.text((1100, 960),  str(kg_return_p) +"%", (255, 255, 255), font=Viga)
drop_sizeW.text((850, 960),  str(kpi.w_drop_size) +" Kg", (255, 255, 255), font=Viga)



img.save('../Images/dashboard.png')