import pyodbc as db
import pandas as pd
import matplotlib.pyplot as plt

conn = db.connect('DRIVER={SQL Server};'
                  'SERVER=10.168.2.168;'
                  'DATABASE=TCPL_SECONDARY;'
                  'UID=sa;'
                  'PWD=erp;')

# # -------- Total value and Weight Target  -----------------------------------
# # ---------------------------------------------------------------------------
# target_df = pd.read_sql_query(""" select  isnull(sum(targetvalue), 0) as TargetVal,
#                 sum((targetqty)*Weight)/1000 as TargetKg
#                 from TargetDistributionItemBySR
#                 left join Hierarchy_SKU
#                 on TargetDistributionItemBySR.SKUID =Hierarchy_SKU.SKUID
#                 where srid = '22'and yearmonth = 202009 --convert(varchar(6),DATEADD(D,0,GETDATE()),112)
#                 """, conn)
#
# total_val_target = int(target_df.TargetVal)
# total_weight_target = int(target_df.TargetKg)


# # ---------- Total Sales in KG and Values -----------------------------------------
# # ---------------------------------------------------------------------------------

# total_sales_df = pd.read_sql_query(""" select SUM(Quantity*Weight)/1000 as SalesKg, sum(Quantity*InvoicePrice) as SalesVal from
#                 (select item.*,SRID, InvoiceDate, Weight from
#                 (select invoiceid, InvoiceDate , SRID from SalesInvoices where InvoiceDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
#                 and convert(varchar(10),DATEADD(D,0,GETDATE()),126)
#                 ) as Sales
#                 inner join
#                 (select invoiceid,Quantity, InvoicePrice, skuid from SalesInvoiceItem) as item
#                 on sales.invoiceid=item.invoiceid
#                 left join Hierarchy_SKU
#                 on item.SKUID = Hierarchy_SKU.SKUID
#                 ) as tbl""", conn)
#
# total_val_sales = int(total_sales_df.SalesVal)
# total_weight_sales = int(total_sales_df.SalesKg)

# # ------------------- Total Returns in Kg and Values ----------------------------------
# # -------------------------------------------------------------------------------------

# return_df = pd.read_sql_query(""" select sum(Quantity*InvoicePrice) as ReturnVal , sum(Quantity*Weight)/100 as ReturnKg from MarketReturns
#             left join
#             MarketReturnItem
#             on MarketReturns.MarketReturnID = MarketReturnItem.MarketReturnID
#             left join Hierarchy_SKU
#             on MarketReturnItem.SKUID = Hierarchy_SKU.SKUID
#             where SRID=22
#
#                         """, conn)
# total_val_return = sum(return_df.ReturnVal)
# total_weight_return = sum(return_df.ReturnKg)

