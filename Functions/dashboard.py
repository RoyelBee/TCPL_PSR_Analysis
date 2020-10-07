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

Stencil_Regular = ImageFont.truetype("../font_styles/Lobster-Regular.ttf", 60, encoding="unic")
Viga = ImageFont.truetype("../font_styles/Viga-Regular.ttf", 30, encoding="unic")

Name = kpi.sr_name
designation = kpi.designation
reporting_boss = kpi.reporting_boss

name.text((66, 15), Name , (255, 255, 255), font=Stencil_Regular)
desig.text((66, 100), designation , (255, 255, 255), font=Viga)
boss.text((280, 165), reporting_boss , (255, 255, 255), font=Viga)


dateL.text((1050, 50), str(day) , (29, 34, 105), font=Viga)
timeL.text((1050, 137), str(time) , (29, 34, 105), font=Viga)
# timestore.text((25, 435), time + "\n" + day, (255, 255, 255), font=font2)
img.save('../Images/dashboard.png')