import os
import smtplib
from _datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pandas as pd
import Functions.generate_table as tbl
from PIL import Image, ImageDraw, ImageFont
import xlrd
import path
import datetime
from calendar import monthrange

dirpath = os.path.dirname(os.path.realpath(__file__))

date = datetime.datetime.now()
current_day = int(date.strftime("%d")) - 1
days_in_month = max(monthrange(int(date.strftime("%Y")), int(date.strftime("%m"))))

# # ------ Generate all Figures ----------------------------
# ### ----------------Please change SR id in kpi list ------
# # --------------------------------------------------------

import Functions.figures as fg
import Functions.targets as trg
import Functions.returns as re
import Functions.user_profiles as up
import Functions.visit_rates as vr
import Functions.customers as vc
import Functions.strike_days as strike
import Functions.lpcs as lpc
import Functions.invoice as inv
import Functions.drop_size as ds

trg_val = trg.TotalTarget(22)[0]
trg_kg = int(trg.TotalTarget(22)[1])

return_val = re.TotalReturn(22)[0]
return_kg = re.TotalReturn(22)[1]

sr_name = up.UserProfile(22)[0]
reporting_boss = up.UserProfile(22)[1]
total_brand = up.UserProfile(22)[2]
designation = up.UserProfile(22)[3]
sales_val_list = up.UserProfile(22)[4]
sales_val = sum(sales_val_list)
sales_kg_list = up.UserProfile(22)[5]
sales_kg = int(sum(sales_kg_list))
brand_list = up.UserProfile(22)[6]
target_list = up.UserProfile(22)[7]
target_kg_list = up.UserProfile(22)[8]

branch_mtd_target_list = []
for i in range(len(target_list)):
    d = (target_list[i] / days_in_month) * current_day
    branch_mtd_target_list.append(d)

branch_mtd_target_kg_list = []
for i in range(len(target_list)):
    kg = (target_kg_list[i] / days_in_month) * current_day
    branch_mtd_target_kg_list.append(kg)

visit_days = vr.VisitRate(22)[0]
SalesCustomer = vr.VisitRate(22)[1]
VisitedCustomer = vr.VisitRate(22)[2]

total_cust = vc.TotalCust(22)
effective_cust = vc.EffectiveCust(22)
visited_cust = vc.VisitCust(22)

visit_rate = round((visited_cust / total_cust) * 100, 2)

vl = ((SalesCustomer / VisitedCustomer) * 100).tolist()
day_visit_rate = []
for i in range(len(vl)):
    day_visit_rate.append(int(vl[i]))

strike_days = strike.StrikeDays(22)[0]
effective_strike = strike.StrikeDays(22)[1]
totalCustomer_strike = strike.StrikeDays(22)[2]

strike_rate = round((effective_cust / total_cust) * 100, 2)

sr = ((effective_strike / totalCustomer_strike) * 100).tolist()
day_strike_rate = []
for i in range(len(sr)):
    day_strike_rate.append(int(sr[i]))

lpc_days = lpc.DayWiseLPC(22)[0]
lpc_rate = lpc.DayWiseLPC(22)[1]
lpc = round(sum(lpc_days) / len(lpc_rate), 2)

total_invoice = inv.Total_Invoice(22)

drop_days = ds.DayWiseDropSize(22)[0]
drop_size_val = ds.DayWiseDropSize(22)[1]
drop_size_kg = ds.DayWiseDropSize(22)[2]

val_drop_size = int(sales_val / total_invoice)
w_drop_size = round(sales_kg / total_invoice, 2)

each_day_sales = sales_val / int(current_day)
each_day_sales_kg = sales_kg / int(current_day)

trend_val = round((each_day_sales * days_in_month), 2)
trend_w_kg = round((each_day_sales_kg * days_in_month), 2)

w_trend_per = 0
if trg_kg == 0:
    w_trend_per = 0
else:
    w_trend_per = round((trend_w_kg / trg_kg) * 100, 2)

# # ------------------------------- KPI Data generation -------------------------------------------------
import Functions.dashboard as dash
import Functions.sales_figure as salesf
import Functions.sales_kg_figure as saleskg
import Functions.visit_rate_figure as visit_fig

dash.generate_dashboard(sr_name, reporting_boss, trg_val, sales_val, trg_kg, sales_kg, days_in_month,
                        current_day, trend_val, return_val, return_kg, visit_rate, strike_rate, lpc, val_drop_size,
                        w_drop_size, trend_w_kg, w_trend_per)

salesf.sales_val_chart(brand_list, sales_val_list, branch_mtd_target_list)
saleskg.sales_kg_chart(brand_list, sales_kg_list, branch_mtd_target_kg_list)
visit_fig.day_wise_visit_rate(visit_days, day_visit_rate)

# fg.day_wise_strike_rate()
# fg.day_wise_lpc_rate()
# fg.day_wise_drop_size_value()

# fg.day_wise_drop_size_kg()


# ----- Join Brands wise Sales Images ---------------------
# brand_sales_val = Image.open(dirpath + "./Images/brand_wise_sales_val.png")
# widthx, heightx = brand_sales_val.size
# brand_sales_kg = Image.open(dirpath + "./Images/brand_wise_sales_kg.png")
#
# imageSize = Image.new('RGB', (1283, 481))
# imageSize.paste(brand_sales_val, (1, 0))
# imageSize.paste(brand_sales_kg, (widthx + 2, 0))
# imageSize.save(dirpath + "./Images/brand_sales.png")
#
# # # ------Add border of visit size  --------------------------------
# day_wise_visit_rate = Image.open(dirpath + "./Images/day_wise_visit_rate.png")
# widthx, heightx = day_wise_visit_rate.size
# imageSize = Image.new('RGB', (1283, 481))
# imageSize.paste(day_wise_visit_rate, (1, 0))
# imageSize.save(dirpath + "./Images/day_wise_visit_rate.png")
#
# # # ------Add border of visit size  --------------------------------
# day_wise_strike_rate = Image.open(dirpath + "./Images/day_wise_strike_rate.png")
# widthx, heightx = day_wise_strike_rate.size
# imageSize = Image.new('RGB', (1283, 481))
# imageSize.paste(day_wise_strike_rate, (1, 0))
# imageSize.save(dirpath + "./Images/day_wise_strike_rate.png")
#
# # # ------Add border of day_wise_lpc_rate size  --------------------------------
# day_wise_lpc_rate = Image.open(dirpath + "./Images/day_wise_lpc_rate.png")
# widthx, heightx = day_wise_strike_rate.size
# imageSize = Image.new('RGB', (1283, 481))
# imageSize.paste(day_wise_lpc_rate, (1, 0))
# imageSize.save(dirpath + "./Images/day_wise_lpc_rate.png")
#
# # # ------Add border of day_wise_drop_size_val size  --------------------------------
# day_wise_drop_size_val = Image.open(dirpath + "./Images/day_wise_drop_size_val.png")
# widthx, heightx = day_wise_drop_size_val.size
# imageSize = Image.new('RGB', (1283, 481))
# imageSize.paste(day_wise_drop_size_val, (1, 0))
# imageSize.save(dirpath + "./Images/day_wise_drop_size_val.png")
#
# # # ------Add border of day_wise_drop_size_val size  --------------------------------
# # day_wise_drop_size_kg = Image.open(dirpath + "./Images/day_wise_drop_size_kg.png")
# # widthx, heightx = day_wise_drop_size_kg.size
# # imageSize = Image.new('RGB', (1283, 481))
# # imageSize.paste(day_wise_drop_size_kg, (1, 0))
# # imageSize.save(dirpath + "./Images/day_wise_drop_size_kg.png")
#
#
# msgRoot = MIMEMultipart('related')
# me = 'erp-bi.service@transcombd.com'
# to = ['', '']  ## al.sahriar@transcombd.com
# cc = ['', '']
# bcc = ['rejaul.islam@transcombd.com', '']
#
# # to = ['biswas@transcombd.com']
# # cc = ['yakub@transcombd.com', 'tawhid@transcombd.com', 'zubair@transcombd.com']
# # bcc = ['aftab.uddin@transcombd.com', 'rejaul.islam@transcombd.com', 'din.mohammad@transcombd.com']
#
# recipient = to + cc + bcc
# from datetime import datetime
#
# date = datetime.today()
# today = str(date.day) + '-' + str(date.strftime("%b")) + '-' + str(date.year) + ' ' + date.strftime("%I:%M %p")
# today1 = str(date.day) + '-' + str(date.strftime("%b")) + '-' + str(date.year)
#
# # # ------------ Group email --------------------
# subject = "TCPL - Secondary Analysis " + today
# email_server_host = 'mail.transcombd.com'
# port = 25
#
# msgRoot['From'] = me
# msgRoot['To'] = ', '.join(to)
# msgRoot['Cc'] = ', '.join(cc)
# msgRoot['Bcc'] = ', '.join(bcc)
# msgRoot['Subject'] = subject
#
# msgAlternative = MIMEMultipart('alternative')
# msgRoot.attach(msgAlternative)
# msgText = MIMEText('This is the alternative plain text message.')
# msgAlternative.attach(msgText)
#
# # # Mail Body
#
# msgText = MIMEText("""
#              <img src="cid:dash" height='1000', width='1280'> <br>
#              <img src="cid:brand" > <br>
#              <img src="cid:visit" > <br>
#              <img src="cid:strike" > <br>
#              <img src="cid:lpc" > <br>
#              <img src="cid:ds_val" > <br>
#
#              <br> """ + tbl.all_table + """
#
#              <h4> This report is system generated. If you have any query please contact with AI Team.  </h4>
#              <img src="cid:logo" height='150' width='250'> <br>
#
#              """, 'html')
# msgAlternative.attach(msgText)
#
# # Attached top 10 leave
# part = MIMEBase('application', "octet-stream")
# file_location = path.get_directory() + './Data/sku_wise_target_sales.xlsx'
#
# filename = os.path.basename(file_location)
# attachment = open(file_location, "rb")
# part = MIMEBase('application', 'octet-stream')
# part.set_payload(attachment.read())
# encoders.encode_base64(part)
# part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
# msgRoot.attach(part)
#
# # # -------- Dashboard --------------------------------------
# fp = open(dirpath + './Images/dashboard.png', 'rb')
# dash = MIMEImage(fp.read())
# fp.close()
#
# dash.add_header('Content-ID', '<dash>')
# msgRoot.attach(dash)
#
# # # -------- Brand wise sales chart -------------------------
# fp = open(dirpath + './Images/brand_sales.png', 'rb')
# brand = MIMEImage(fp.read())
# fp.close()
#
# brand.add_header('Content-ID', '<brand>')
# msgRoot.attach(brand)
#
# # # ------- Day wise Visit Rate -----------------------------
# fp = open(dirpath + '/Images/day_wise_visit_rate.png', 'rb')
# visit = MIMEImage(fp.read())
# fp.close()
#
# visit.add_header('Content-ID', '<visit>')
# msgRoot.attach(visit)
#
# # # ------- Day wise Strike rate ----------------------------
# fp = open(dirpath + '/Images/day_wise_strike_rate.png', 'rb')
# strike = MIMEImage(fp.read())
# fp.close()
#
# strike.add_header('Content-ID', '<strike>')
# msgRoot.attach(strike)
#
# # # ------ Day wise LPC -----------------------------------
# fp = open(dirpath + '/Images/day_wise_lpc_rate.png', 'rb')
# lpc = MIMEImage(fp.read())
# fp.close()
#
# lpc.add_header('Content-ID', '<lpc>')
# msgRoot.attach(lpc)
#
# # # ------ Day wise Drop Size Value -------------------------
# fp = open(dirpath + '/Images/day_wise_drop_size_val.png', 'rb')
# ds_val = MIMEImage(fp.read())
# fp.close()
#
# ds_val.add_header('Content-ID', '<ds_val>')
# msgRoot.attach(ds_val)
#
# # # Attached Logo -------------------------------------------
# fp = open(dirpath + './Images/AI TEAM.png', 'rb')
# logo = MIMEImage(fp.read())
# fp.close()
#
# logo.add_header('Content-ID', '<logo>')
# msgRoot.attach(logo)
#
# # #-------Finally send mail and close server connection -----
# server = smtplib.SMTP(email_server_host, port)
# server.ehlo()
# print('------------------')
# print('Sending Mail')
# server.sendmail(me, recipient, msgRoot.as_string())
# print('Mail Send')
# print('-----------------')
# server.close()
