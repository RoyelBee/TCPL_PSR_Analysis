import pyodbc as db
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from calendar import monthrange

conn = db.connect('DRIVER={SQL Server};'
                  'SERVER=10.168.2.168;'
                  'DATABASE=TCPL_SECONDARY;'
                  'UID=sa;'
                  'PWD=erp;')

# # -------- Total value and Weight Target  -----------------------------------
# # ---------------------------------------------------------------------------
target_df = pd.read_sql_query(""" select  isnull(sum(targetvalue), 0) as TargetVal,
                sum((targetqty)*Weight)/1000 as TargetKg
                from TargetDistributionItemBySR
                left join Hierarchy_SKU
                on TargetDistributionItemBySR.SKUID =Hierarchy_SKU.SKUID
                where srid = '22'and yearmonth = 202009 --convert(varchar(6),DATEADD(D,0,GETDATE()),112)
                """, conn)

total_val_target = int(target_df.TargetVal)
total_weight_target = int(target_df.TargetKg)

# ---------- Total Sales in KG and Values -----------------------------------------
# ---------------------------------------------------------------------------------

total_sales_df = pd.read_sql_query(""" select SUM(Quantity*Weight)/1000 as SalesKg, sum(Quantity*InvoicePrice) as SalesVal from
                (select item.*,SRID, InvoiceDate, Weight from
                (select invoiceid, InvoiceDate , SRID from SalesInvoices where InvoiceDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                and convert(varchar(10),DATEADD(D,0,GETDATE()),126)
                ) as Sales
                inner join
                (select invoiceid,Quantity, InvoicePrice, skuid from SalesInvoiceItem) as item
                on sales.invoiceid=item.invoiceid
                left join Hierarchy_SKU
                on item.SKUID = Hierarchy_SKU.SKUID
                ) as tbl""", conn)

total_val_sales = int(total_sales_df.SalesVal)
total_weight_sales = int(total_sales_df.SalesKg)

# ------------------- Total Returns in Kg and Values ----------------------------------
# -------------------------------------------------------------------------------------

return_df = pd.read_sql_query(""" select sum(Quantity*InvoicePrice) as ReturnVal , sum(Quantity*Weight)/100 as ReturnKg from MarketReturns
            left join
            MarketReturnItem
            on MarketReturns.MarketReturnID = MarketReturnItem.MarketReturnID
            left join Hierarchy_SKU
            on MarketReturnItem.SKUID = Hierarchy_SKU.SKUID
            where SRID=22

                        """, conn)
total_val_return = sum(return_df.ReturnVal)
total_weight_return = sum(return_df.ReturnKg)

sales_achievement = (total_val_sales / total_val_target) * 100
weight_achievement = (total_weight_sales / total_weight_target) * 100

# # -------- Cumulative Target  and sales --------------------------------------
# # ----------------------------------------------------------------------------
date = datetime.datetime.now()
current_day = date.strftime("%d")
days_in_month = max(monthrange(int(date.strftime("%Y")), int(date.strftime("%m"))))

cu = []
i = 0
for i in range(days_in_month):
    val = int(total_val_target / days_in_month)
    cu.append(val)


def Cumulative(val):
    new = []
    cumsum = 0
    for element in val:
        cumsum += element
        new.append(cumsum)
    return new


cumulativeTarget = Cumulative(cu)
cumulativeTarget = cumulativeTarget[:int(days_in_month)]


# # ----------- Sales ----------------------------------------------------

day_wise_sales_df = pd.read_sql_query("""select right(left(left(InvoiceDate, 10),6),2) Date, SUM(Quantity) as SalesQty,SUM(Quantity*Weight)/1000 as SalesKg, sum(Quantity*InvoicePrice) as SalesVal from
                    (select item.*,SRID, InvoiceDate from
                    (select invoiceid, InvoiceDate , SRID from SalesInvoices where InvoiceDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                    and convert(varchar(10),DATEADD(D,0,GETDATE()),126)
                    ) as Sales
                    inner join
                    (select invoiceid,Quantity, Weight, InvoicePrice from SalesInvoiceItem 
                    left join Hierarchy_SKU
                    on SalesInvoiceItem.SKUID = Hierarchy_SKU.SKUID
                    ) as item
                    on sales.invoiceid=item.invoiceid where SRID=22) as fwe
                    group by left(InvoiceDate, 10) """, conn)

days = day_wise_sales_df.Date.tolist()
day_salesVal = day_wise_sales_df.SalesVal.tolist()
day_salesKg = day_wise_sales_df.SalesKg.tolist()


cumulativeWeight = Cumulative(day_salesKg)
cumulativeWeight = cumulativeTarget[:int(current_day)]


cumulativeSalesVal = Cumulative(day_salesVal)
cumulativeSalesVal = cumulativeSalesVal[:int(current_day)]