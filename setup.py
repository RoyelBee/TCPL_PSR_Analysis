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
import xlrd
import path

import Functions.dashboard
dirpath = os.path.dirname(os.path.realpath(__file__))

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
             
             <img src="cid:dash" height='1000'> <br>
             <br> """ + tbl.all_table + """
             
             <h4> This report is system generated. If you have any query please contact with AI Team.  </h4> 
             <img src="cid:logo" height='150'> <br>

             """, 'html')
msgAlternative.attach(msgText)

# # Attached top 10 leave
# part = MIMEBase('application', "octet-stream")
# file_location = path.get_directory() + './Data/top10_leave_taker.xlsx'
# filename = os.path.basename(file_location)
# attachment = open(file_location, "rb")
# part = MIMEBase('application', 'octet-stream')
# part.set_payload(attachment.read())
# encoders.encode_base64(part)
# part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
# msgRoot.attach(part)

# # -------- Dashboard ----------------------------
fp = open(dirpath + './Images/dashboard.png', 'rb')
dash = MIMEImage(fp.read())
fp.close()

dash.add_header('Content-ID', '<dash>')
msgRoot.attach(dash)

# # Attached Logo ------------------------------
fp = open(dirpath + './Images/AI TEAM.png', 'rb')
logo = MIMEImage(fp.read())
fp.close()

logo.add_header('Content-ID', '<logo>')
msgRoot.attach(logo)

# #----------- Finally send mail and close server connection -----
server = smtplib.SMTP(email_server_host, port)
server.ehlo()
print('\n-----------------')
print('Sending Mail')
server.sendmail(me, recipient, msgRoot.as_string())
print('Mail Send')
print('-------------------')
server.close()
