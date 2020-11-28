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
import numpy as np

def generate_data():
    conn = db.connect('DRIVER={SQL Server};'
                      'SERVER=--------------;'
                      'DATABASE=TCPL_SECONDARY;'
                      'UID=--;'
                      'PWD=---;')

    sku_df = pd.read_sql_query(""" 
            DECLARE @date date = GETDATE(); 
            declare @current_day int = right(convert(varchar(8),getdate(), 112), 2)
                            
            select srItnameTarget.Item, srItnameTarget.skuname,
            [Months Target(Tk)], 
            [MTD Target(Tk)], 
            isnull([MTD Sales(Tk)], 0) as [MTD Sales(Tk)],
            --(isnull([Months Sales(Tk)], 0)/[MTD Target(Tk)]) as 'achiv %',
            [Months Target(Kg)],
            [MTD Target(Kg)], 
            [MTD Sales(Kg)]
            from
            (select targetsr.srid,srname,sku.skuid as Item, sku.ShortName as skuname,sum(TargetValue) as [Months Target(Tk)],
            cast((sum(TargetValue) /  cast(DAY(EOMONTH ( @date )) as int)) * @current_day as int) as [MTD Target(Tk)],
            sum(TargetQty*Weight)/1000 as [Months Target(Kg)], 
            cast((((sum(TargetQty*Weight)/1000)/ cast(DAY(EOMONTH ( @date )) as int)) * @current_day) as int) as [MTD Target(Kg)]
            from 
            (Select * from TargetDistributionItemBySR where yearmonth = convert(varchar(6),DATEADD(D,0,GETDATE()),112) and srid=22) as targetsr
            left join 
            (select * from Hierarchy_Emp) as emp
            on targetsr.srid=emp.SRID
            left join 
            (select * from Hierarchy_SKU) as Sku
            on sku.SKUID=targetsr.SKUID
            group by srname,sku.skuid,shortname, targetsr.srid
            ) as srItnameTarget
            right join 
            (select salesitem.SRID,srname,sku.skuid as Item,isnull(sum((Quantity-FreeQty)*InvoicePrice), 0) as [MTD Sales(Tk)],
            isnull(sum((Quantity-FreeQty)*Weight)/1000, 0) as [MTD Sales(Kg)] from 
            (selecT Item.*,Srid from 
            (select * from SalesInvoices where InvoiceDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
            and convert(varchar(10),DATEADD(D,0,GETDATE()),126) and srid=22) as Sale
            inner join 
            (select * from SalesInvoiceItem) as Item
            on sale.InvoiceID=item.InvoiceID) as salesitem
            left join 
            (select * from Hierarchy_Emp) as emp
            on salesitem.srid=emp.SRID
            left join 
            (select * from Hierarchy_SKU) as Sku
            on sku.SKUID=salesitem.SKUID
            group by srname,sku.skuid,salesitem.SRID) as srItnamesale
            on srItnameTarget.srid=srItnamesale.srid
            and srItnameTarget.Item=srItnamesale.Item """, conn)

    sku_df['Achiv%(Tk)'] = (sku_df['MTD Sales(Tk)'] / sku_df['MTD Target(Tk)'] * 100).replace([np.inf], 0)
    sku_df['Achiv%(Kg)'] = (sku_df['MTD Sales(Kg)'] / sku_df['MTD Target(Kg)'] * 100).replace([np.inf], 0)

    sku_df.to_excel('./Data/sku_wise_target_sales.xlsx', index=False)
    print('SKU wise target and sales data saved')

def comma_seperator(value):
    if (len(value) > 6):
        return str(value[0:len(value) - 6] + "," + value[len(value) - 6:len(value) - 3] + ","
                   + value[len(value) - 3:len(value)])
    elif (len(value) > 3):
        return str(value[0:len(value) - 3] + "," + value[len(value) - 3:len(value)])
    elif (len(value) > 0):
        return value
    else:
        return "-"



def get_SKU_wise_target_sales_Table():
    generate_data()
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
            td = td + "<td class=\"right\"  >" + comma_seperator(str(int(sh.cell_value(i, j)))) + "</td>\n"

        for j in range(3, 4):
            td = td + "<td class=\"right\" >" + comma_seperator(str(int(sh.cell_value(i, j)))) + "</td>\n"

        for j in range(4, 5):
            td = td + "<td class=\"right\">" + comma_seperator(str(int(sh.cell_value(i, j)))) + "</td>\n"

        for j in range(5, 6):
            td = td + "<td class=\"right\">" + comma_seperator(str(sh.cell_value(i, j))) + "</td>\n"

        for j in range(6, 7):
            td = td + "<td class=\"right\">" + comma_seperator(str(int(sh.cell_value(i, j)))) + "</td>\n"

        for j in range(7, 8):
            td = td + "<td class=\"right\">" + comma_seperator(str(int(sh.cell_value(i, j)))) + "</td>\n"

        for j in range(8, 9):
            td = td + "<td class=\"right\">" + str(round(sh.cell_value(i, j), 2))+'%'+ "</td>\n"

        for j in range(9, 10):
            td = td + "<td class=\"right\">" + str(round(sh.cell_value(i, j), 2))+'%' + "</td>\n"

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
                    background-color:#52fbe2;
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
            <table style="width:100%">
                    <p style="text-align:left"> """ + get_SKU_wise_target_sales_Table() + """</p>
            </table>
            
        </body>
        </html>
         """
