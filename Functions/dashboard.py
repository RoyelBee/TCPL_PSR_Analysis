from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import pyodbc as db
from datetime import datetime
import datetime as dd
import pytz

# # --------- Import local files -----------------
import Functions.kpi as kpi
import math
def generate_dashboard():
    date = datetime.today()
    day = str(date.day) + '/' + str(date.month) + '/' + str(date.year)
    tz_NY = pytz.timezone('Asia/Dhaka')
    datetime_BD = datetime.now(tz_NY)
    time = datetime_BD.strftime("%I:%M %p")
    date = datetime.today()
    x = dd.datetime.now()
    day = str(date.day) + '-' + str(x.strftime("%b")) + '-' + str(date.year)
    tz_NY = pytz.timezone('Asia/Dhaka')
    datetime_BD = datetime.now(tz_NY)
    time = datetime_BD.strftime("%I:%M %p")

    img = Image.open("./Images/dash_structure.png")
    name = ImageDraw.Draw(img)
    boss = ImageDraw.Draw(img)
    dateL = ImageDraw.Draw(img)
    timeL = ImageDraw.Draw(img)
    targetL = ImageDraw.Draw(img)
    salesL = ImageDraw.Draw(img)
    trendVal = ImageDraw.Draw(img)
    trendPer = ImageDraw.Draw(img)
    visitV = ImageDraw.Draw(img)
    strike = ImageDraw.Draw(img)
    lpc = ImageDraw.Draw(img)

    drop_size_val = ImageDraw.Draw(img)

    # # ------- Weight Pointer ----------------------
    wTargetL = ImageDraw.Draw(img)
    wSalesL = ImageDraw.Draw(img)
    achivL = ImageDraw.Draw(img)
    returnL = ImageDraw.Draw(img)
    trendW = ImageDraw.Draw(img)
    trendValW = ImageDraw.Draw(img)
    visitW = ImageDraw.Draw(img)

    drop_sizeW = ImageDraw.Draw(img)

    # # ---------------------------------------------

    Stencil_Regular = ImageFont.truetype("./font_styles/Lobster-Regular.ttf", 60, encoding="unic")
    Viga = ImageFont.truetype("./font_styles/Viga-Regular.ttf", 40, encoding="unic")
    timef = ImageFont.truetype("./font_styles/Viga-Regular.ttf", 30, encoding="unic")
    Name = kpi.sr_name
    # designation = kpi.designation
    reporting_boss = kpi.reporting_boss

    # # ------------ Profile section ---------------------------------
    name.text((10, 15), Name, (255, 255, 255), font=Stencil_Regular)
    boss.text((220, 158), reporting_boss, (255, 255, 255), font=timef)
    dateL.text((1050, 50), str(day), (29, 34, 105), font=timef)
    timeL.text((1060, 137), str(time), (29, 34, 105), font=timef)

    # # ------ Value Section  ----------------------------------------
    mtd_target = int((kpi.total_val_target / kpi.days_in_month) * kpi.current_day)
    target = kpi.currency_converter(mtd_target)
    sales = kpi.currency_converter(kpi.sales_val)

    if kpi.total_val_target == 0:
        achiv = 0
    else:
        achiv = round((kpi.sales_val / kpi.total_val_target) * 100, 2)

    trendval = kpi.currency_converter(int(kpi.trend_val))

    if (kpi.trend_val == 0 & kpi.total_val_target == 0):
        trend_percent = 0
    else:
        trend_percent = round((kpi.trend_val/kpi.total_val_target) * 100, 2)

    targetL.text((70, 400), str(target), (255, 255, 255), font=Viga)
    salesL.text((330, 400), str(sales), (255, 255, 255), font=Viga)
    achivL.text((580, 400), str(achiv) + "%", (255, 255, 255), font=Viga)
    trendVal.text((850, 400), str(trendval), (255, 255, 255), font=Viga)
    trendPer.text((1090, 400), str(trend_percent) + "%", (255, 255, 255), font=Viga)

    if (kpi.total_val_return == 0):
        val_return_p = 0
    else:
        val_return_p = round((kpi.total_val_return / kpi.sales_val) * 100, 2)

    visitV.text((70, 550), str(kpi.visit_rate) + '%', (255, 255, 255), font=Viga)
    strike.text((330, 550), str(kpi.strike_rate) + '%', (255, 255, 255), font=Viga)
    lpc.text((605, 550), str(kpi.lpc), (255, 255, 255), font=Viga)
    drop_size_val.text((850, 550), str( round((kpi.val_drop_size/1000), 2)) + 'K', (255, 255, 255), font=Viga)
    returnL.text((1090, 550), str(val_return_p) + "%", (255, 255, 255), font=Viga)

    # # --------- Weight wise KPI -------------------------------------------
    mtd_weight_target = int((kpi.total_weight_target / kpi.days_in_month) * kpi.current_day)

    if (kpi.total_weight_target == 0 & kpi.sales_kg == 0):
        achivKg = 0
    else:
        achivKg = round((kpi.sales_kg / kpi.total_weight_target) * 100, 2)

    if kpi.total_weight_return == 0:
        kg_return_p = 0
    else:
        kg_return_p = round((kpi.total_weight_return / kpi.sales_kg) * 100, 2)

    wTargetL.text((70, 790), str(mtd_weight_target) + 'Kg', (255, 255, 255), font=Viga)
    wSalesL.text((330, 790), str(kpi.sales_kg) + 'Kg', (255, 255, 255), font=Viga)
    achivL.text((580, 790), str(achivKg) + "%", (255, 255, 255), font=Viga)
    trendW.text((850, 790), str(int(kpi.trend_w_kg)) + 'Kg', (255, 255, 255), font=Viga)
    trendValW.text((1090, 790), str(kpi.w_trend_per) + "%", (255, 255, 255), font=Viga)

    visitW.text((70, 960), str(kpi.visit_rate) + "%", (255, 255, 255), font=Viga)
    strike.text((330, 960), str(kpi.strike_rate) + '%', (255, 255, 255) , font=Viga)
    strike.text((605, 960), str(kpi.lpc), (255, 255, 255), font=Viga)
    drop_sizeW.text((850, 960), str(kpi.w_drop_size) + "Kg", (255, 255, 255), font=Viga)
    returnL.text((1090, 960), str(kg_return_p) + "%", (255, 255, 255), font=Viga)


    return img.save('./Images/dashboard.png')
