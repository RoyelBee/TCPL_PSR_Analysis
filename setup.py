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

dirpath = os.path.dirname(os.path.realpath(__file__))

# # ------ Generate all Figures ----------------------------
import Functions.figures as fg
import Functions.dashboard as dash

dash.generate_dashboard()
fg.sales_val_chart()
fg.sales_kg_chart()
fg.day_wise_visit_rate()
fg.day_wise_strike_rate()
fg.day_wise_lpc_rate()
fg.day_wise_drop_size_value()
# fg.day_wise_drop_size_kg()


# ---------------------------------------------------------

# ----- Join Brands wise Sales Images ---------------------
brand_sales_val = Image.open(dirpath + "./Images/brand_wise_sales_kg.png")
widthx, heightx = brand_sales_val.size
brand_sales_kg = Image.open(dirpath + "./Images/brand_wise_sales_val.png")

imageSize = Image.new('RGB', (1283, 481))
imageSize.paste(brand_sales_val, (1, 0))
imageSize.paste(brand_sales_kg, (widthx + 2, 0))
imageSize.save(dirpath + "./Images/brand_sales.png")

# # ------Add border of visit size  --------------------------------
day_wise_visit_rate = Image.open(dirpath + "./Images/day_wise_visit_rate.png")
widthx, heightx = day_wise_visit_rate.size
imageSize = Image.new('RGB', (1283, 481))
imageSize.paste(day_wise_visit_rate, (1, 0))
imageSize.save(dirpath + "./Images/day_wise_visit_rate.png")

# # ------Add border of visit size  --------------------------------
day_wise_strike_rate = Image.open(dirpath + "./Images/day_wise_strike_rate.png")
widthx, heightx = day_wise_strike_rate.size
imageSize = Image.new('RGB', (1283, 481))
imageSize.paste(day_wise_strike_rate, (1, 0))
imageSize.save(dirpath + "./Images/day_wise_strike_rate.png")

# # ------Add border of day_wise_lpc_rate size  --------------------------------
day_wise_lpc_rate = Image.open(dirpath + "./Images/day_wise_lpc_rate.png")
widthx, heightx = day_wise_strike_rate.size
imageSize = Image.new('RGB', (1283, 481))
imageSize.paste(day_wise_lpc_rate, (1, 0))
imageSize.save(dirpath + "./Images/day_wise_lpc_rate.png")

# # ------Add border of day_wise_drop_size_val size  --------------------------------
day_wise_drop_size_val = Image.open(dirpath + "./Images/day_wise_drop_size_val.png")
widthx, heightx = day_wise_drop_size_val.size
imageSize = Image.new('RGB', (1283, 481))
imageSize.paste(day_wise_drop_size_val, (1, 0))
imageSize.save(dirpath + "./Images/day_wise_drop_size_val.png")

# # ------Add border of day_wise_drop_size_val size  --------------------------------
# day_wise_drop_size_kg = Image.open(dirpath + "./Images/day_wise_drop_size_kg.png")
# widthx, heightx = day_wise_drop_size_kg.size
# imageSize = Image.new('RGB', (1283, 481))
# imageSize.paste(day_wise_drop_size_kg, (1, 0))
# imageSize.save(dirpath + "./Images/day_wise_drop_size_kg.png")


msgRoot = MIMEMultipart('related')
me = 'erp-bi.service@transcombd.com'
to = ['rejaul.islam@transcombd.com', '']
cc = ['', '']
bcc = ['', '']

# to = ['biswas@transcombd.com']
# cc = ['yakub@transcombd.com', 'tawhid@transcombd.com', 'zubair@transcombd.com']
# bcc = ['aftab.uddin@transcombd.com', 'rejaul.islam@transcombd.com', 'din.mohammad@transcombd.com']

recipient = to + cc + bcc

date = datetime.today()
today = str(date.day) + '-' + str(date.strftime("%b")) + '-' + str(date.year) + ' ' + date.strftime("%I:%M %p")
today1 = str(date.day) + '-' + str(date.strftime("%b")) + '-' + str(date.year)

# # ------------ Group email --------------------
subject = "ERP Members Leave and Late Analysis " + today
email_server_host = 'mail.transcombd.com'
port = 25

msgRoot['From'] = me
msgRoot['To'] = ', '.join(to)
msgRoot['Cc'] = ', '.join(cc)
msgRoot['Bcc'] = ', '.join(bcc)
msgRoot['Subject'] = subject

msgAlternative = MIMEMultipart('alternative')
msgRoot.attach(msgAlternative)
msgText = MIMEText('This is the alternative plain text message.')
msgAlternative.attach(msgText)

# # Mail Body

msgText = MIMEText("""
            <h3 style="color:red;"> Attention Check the Design. Data will be mis-matched. </h3>
             <img src="cid:dash" height='1000', width='1280'> <br>
             <img src="cid:brand" > <br>
             <img src="cid:visit" > <br>
             <img src="cid:strike" > <br>
             <img src="cid:lpc" > <br>
             <img src="cid:ds_val" > <br>

             <br> """ + tbl.all_table + """

             <h4> This report is system generated. If you have any query please contact with AI Team.  </h4>
             <img src="cid:logo" height='150' width='250'> <br>

             """, 'html')
msgAlternative.attach(msgText)

# Attached top 10 leave
part = MIMEBase('application', "octet-stream")
file_location = path.get_directory() + './Data/sku_wise_target_sales.xlsx'
filename = os.path.basename(file_location)
attachment = open(file_location, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msgRoot.attach(part)

# # -------- Dashboard ----------------------------
fp = open(dirpath + './Images/dashboard.png', 'rb')
dash = MIMEImage(fp.read())
fp.close()

dash.add_header('Content-ID', '<dash>')
msgRoot.attach(dash)

# # -------- Brand wise sales chart ---------------
fp = open(dirpath + './Images/brand_sales.png', 'rb')
brand = MIMEImage(fp.read())
fp.close()

brand.add_header('Content-ID', '<brand>')
msgRoot.attach(brand)

# # ------- Day wise Visit Rate -----------------------------
fp = open(dirpath + '/Images/day_wise_visit_rate.png', 'rb')
visit = MIMEImage(fp.read())
fp.close()

visit.add_header('Content-ID', '<visit>')
msgRoot.attach(visit)

## ------- Day wise Strike rate ----------------------------
fp = open(dirpath + '/Images/day_wise_strike_rate.png', 'rb')
strike = MIMEImage(fp.read())
fp.close()

strike.add_header('Content-ID', '<strike>')
msgRoot.attach(strike)


# # ------ Day wise LPC -----------------------------------
fp = open(dirpath + '/Images/day_wise_lpc_rate.png', 'rb')
lpc = MIMEImage(fp.read())
fp.close()

lpc.add_header('Content-ID', '<lpc>')
msgRoot.attach(lpc)

# # ------ Day wise Drop Size Value -----------------------------------
fp = open(dirpath + '/Images/day_wise_drop_size_val.png', 'rb')
ds_val = MIMEImage(fp.read())
fp.close()

ds_val.add_header('Content-ID', '<ds_val>')
msgRoot.attach(ds_val)


# # Attached Logo ------------------------------
fp = open(dirpath + './Images/AI TEAM.png', 'rb')
logo = MIMEImage(fp.read())
fp.close()

logo.add_header('Content-ID', '<logo>')
msgRoot.attach(logo)

# #----------- Finally send mail and close server connection -----
server = smtplib.SMTP(email_server_host, port)
server.ehlo()
print('\n------------------')
print('Sending Mail')
server.sendmail(me, recipient, msgRoot.as_string())
print('Mail Send')
print('-------------------')
server.close()
