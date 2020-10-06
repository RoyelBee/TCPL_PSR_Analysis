import pandas as pd
import openpyxl
import pyodbc as db

import os
import smtplib
from _datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import pandas as pd
import Functions.generate_data as gdata
import xlrd

conn = db.connect('DRIVER={SQL Server};'
                  'SERVER=10.168.2.168;'
                  'DATABASE=TCPL_SECONDARY;'
                  'UID=sa;'
                  'PWD=erp;')

sku_df = pd.read_sql_query("""select item.skuid as SKUID, item.ShortName as [SKU Name],
        isnull(sum(targetv.TargetValue), 0) as [Value Target], isnull(sum(Quantity*InvoicePrice), 0) as [Sales Value],
        
         isnull(sum(targetv.TargetQty*Quantity)/1000, 0) as [Volume Target],
         isnull(sum(Quantity*Weight)/1000, 0) as [Sales Volume] from
        
            (select sales.skuid,Quantity, InvoicePrice from
                (select * from SalesInvoices where SRID=22 and InvoiceDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                    and convert(varchar(10),DATEADD(D,0,GETDATE()),126))as a
                left join
                (select * from SalesInvoiceItem) as sales
                on a.InvoiceID=sales.InvoiceID) as c
                left join
                (select * from Hierarchy_SKU) as item
                on c.skuid=item.skuid
        
                 left join
                 (select * from TargetDistributionItemBySR) as targetv
                 on item.SKUID = targetv.SKUID
        
        group by item.skuid, item.ShortName
        order by [Sales Value] desc """, conn)

sku_df.to_excel('./Data/sku_wise_target_sales.xlsx', index=False)
print('SKU wise target and sales data saved')


def get_SKU_wise_target_sales_Table():
    wb = xlrd.open_workbook('./Data/sku_wise_target_sales.xlsx')
    sh = wb.sheet_by_name('Sheet1')
    th = ""
    td = ""
    for i in range(0, 1):
        th = th + "<tr>\n"
        th = th + "<th class=\"table8head\">SL</th>"
        for j in range(0, sh.ncols):
            th = th + "<th class=\"table8head\" >" + str(sh.cell_value(i, j)) + "</th>\n"
        th = th + "</tr>\n"

    for i in range(1, sh.nrows):
        td = td + "<tr>\n"
        td = td + "<td class=\"idcol\">" + str(i) + "</td>"
        td = td + "</td>"

        for j in range(0, 1):
            td = td + "<td class=\"right\">" + str(int(sh.cell_value(i, j))) + "</td>\n"

        for j in range(1, 2):
            td = td + "<td class=\"unit\">" + str(sh.cell_value(i, j)) + "</td>\n"

        for j in range(2, 3):
            td = td + "<td class=\"right\"  >" + str(int(sh.cell_value(i, j))) + "</td>\n"

        for j in range(3, 4):
            td = td + "<td class=\"right\" >" + str(int(sh.cell_value(i, j))) + "</td>\n"

        for j in range(4, 5):
            td = td + "<td class=\"right\">" + str(int(sh.cell_value(i, j))) + "</td>\n"

        for j in range(5, 6):
            td = td + "<td class=\"right\">" + str(int(sh.cell_value(i, j))) + "</td>\n"

        td = td + "</tr>\n"
    html = th + td
    return html


all_table = """ <!DOCTYPE html>
        <html lang="en">
           <head>
            <style>
                table {
                    font-family: arial, sans-serif;
                    border-collapse: collapse;
                    padding: 0px;
                    white-space: nowrap;
                    font-size: 10px;
                    border: 1px solid black;
                }
                th {
                    color: black;
                    border: 1px solid black;
                    font-size: 14px;
                    padding-left: 5px;
                    padding-right: 5px;
                    height: 50px;
                } 

                .table1head {
                    background-color: #ff6b00;
                } 
                .table2head {
                    background-color: #00ffeb;
                } 
                .table3head {
                    background-color:#e6d400;
                }
                 .table4head {
                    background-color:#ff4e5c;
                }
                  .table5head {
                    background-color:#ff4900;
                }

                  .table6head {
                    background-color:#f1585b;
                } 
                  .table7head {
                    background-color:#2cc238;
                }

                } 
                  .table8head {
                    background-color:#c0b9b9;
                } 

                .sl{
                    background-color: #e5f0e5;
                    padding-right: px;
                    padding-left: 3px;
                    text-align: left;  

                }              
                .item_sl{
                    background-color: #e5f0e5;
                    padding-right: px;
                    padding-left: 3px;
                    text-align: left;  
                    width: 55px;
                }
                .name {
                    background-color: #e5f0e5;
                    font-weight: bold;
                    padding-right: 3px;
                    padding-left: 3px;
                    color: black;
                    text-align: left;
                    width: 180px;
                }                  
                .desig {
                    background-color: #e5f0e5;
                    font-weight: bold;
                    color: black;
                    text-align: left;
                    padding-right: 3px;
                    padding-left: 3px;
                    width: 150px;
                }

                .join_date_and_duration {
                    background-color: #e5f0e5;
                    font-weight: bold;
                    color: black;
                    text-align: left;
                    padding-right: 3px;
                    padding-left: 3px;
                    width: 80px;
                }
                .total_wd {
                    background-color: #e5f0e5;
                    font-weight: bold;
                    color: black;
                    text-align: left;
                    padding-right: 3px;
                    padding-left: 3px;
                    width: 50px;
                }
                .leave{
                    background-color: #e5f0e5;
                    font-weight: bold;
                    color: black;
                    text-align: left;
                    padding-right: 3px;
                    padding-left: 3px;
                    width: 40px;
                }
                .tllal{
                    background-color: #e5f0e5;
                    font-weight: bold;
                    color: black;
                    text-align: left;
                    padding-right: 3px;
                    padding-left: 3px;
                    width: 70px;
                }
                .center{
                    text-align: center;
                    padding-right: 3px;
                    padding-left: 3px;
                }
                .right{
                    text-align: right;
                    padding-right: 5px;
                    padding-left: 5px;
                }
                td {
                    font-family: "Tohoma";
                    border: 1px solid gray;
                    font-size: 12px;
                    padding-right: 3px;
                    padding-left: 3px;
                }


            </style>

        </head>
        <body>


            <h3 style="text-align:left"> Table 01: SKU Wise Target and Sales </h3>
            <table style="width:800px">
                    <p style="text-align:left"> """ + get_SKU_wise_target_sales_Table() + """</p>
            </table>
            
        </body>
        </html>
         """
