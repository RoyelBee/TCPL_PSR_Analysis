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


def currency_converter(num):
    num_size = len(str(num))
    if num_size >= 8:
        number = str(round((num / 10000000), 2)) + ' Cr'
    elif num_size >= 7:
        number = str(round(num / 1000000, 2)) + ' M'
    elif num_size >= 4:
        number = str(round(num / 1000, 2)) + ' K'
    else:
        number = num
    return number


# # -------- Total value and Weight Target  -------------------------------------
# # -----------------------------------------------------------------------------
target_df = pd.read_sql_query(""" select  isnull(sum(targetvalue), 0) as TargetVal,
            isnull(sum((targetqty)*Weight)/1000, 0) as TargetKg
            from TargetDistributionItemBySR
            left join Hierarchy_SKU
            on TargetDistributionItemBySR.SKUID =Hierarchy_SKU.SKUID
            where srid = '22'and yearmonth = 202009 --convert(varchar(6),DATEADD(D,0,GETDATE()),112)
                            """, conn)

total_val_target = int(target_df.TargetVal)
total_weight_target = int(target_df.TargetKg)

# # ---------- Total Sales in KG and Values -----------------------------------------
# # ---------------------------------------------------------------------------------
#
# total_sales_df = pd.read_sql_query(""" select SUM(Quantity*Weight)/1000 as SalesKg, sum(Quantity*InvoicePrice) as SalesVal from
#                 (select item.*,SRID, InvoiceDate, Weight from
#                 (select invoiceid, InvoiceDate , SRID from SalesInvoices
#                 where srid=22 and InvoiceDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
#                 and convert(varchar(10),DATEADD(D,0,GETDATE()),126)
#                 ) as Sales
#                 inner join
#                 (select invoiceid,Quantity, InvoicePrice, skuid from SalesInvoiceItem) as item
#                 on sales.invoiceid=item.invoiceid
#                 left join Hierarchy_SKU
#                 on item.SKUID = Hierarchy_SKU.SKUID
#                 ) as tbl
#                  """, conn)
#
# total_val_sales = int(total_sales_df.SalesVal)
# total_weight_sales = int(total_sales_df.SalesKg)

#
# # ------------------- Total Returns in Kg and Values ----------------------------------
# # -------------------------------------------------------------------------------------

return_df = pd.read_sql_query(""" select isnull(sum(Quantity*InvoicePrice),0) as ReturnVal , 
            isnull(sum(Quantity*Weight)/100, 0) as ReturnKg from MarketReturns
            left join
            MarketReturnItem
            on MarketReturns.MarketReturnID = MarketReturnItem.MarketReturnID
            left join Hierarchy_SKU
            on MarketReturnItem.SKUID = Hierarchy_SKU.SKUID
            where SRID=22 and MarketReturnDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
            and  convert(varchar(10),DATEADD(D,0,GETDATE()),126)
                                    """, conn)
total_val_return = sum(return_df.ReturnVal)
total_weight_return = sum(return_df.ReturnKg)

# sales_achievement = (total_val_sales / total_val_target) * 100
# weight_achievement = (total_weight_sales / total_weight_target) * 100
#
# # # -------- Cumulative Target  and sales --------------------------------------
# # # ----------------------------------------------------------------------------
# date = datetime.datetime.now()
# current_day = date.strftime("%d")
# days_in_month = max(monthrange(int(date.strftime("%Y")), int(date.strftime("%m"))))

# cu = []
# i = 0
# for i in range(days_in_month):
#     val = int(total_val_target / days_in_month)
#     cu.append(val)
#
#
# def Cumulative(val):
#     new = []
#     cumsum = 0
#     for element in val:
#         cumsum += element
#         new.append(cumsum)
#     return new
#
#
# cumulativeTarget = Cumulative(cu)
# cumulativeTarget = cumulativeTarget[:int(days_in_month)]
#
#
# # # ----------- Sales ----------------------------------------------------
#
# day_wise_sales_df = pd.read_sql_query("""select right(left(left(InvoiceDate, 10),6),2) Date, SUM(Quantity) as SalesQty,SUM(Quantity*Weight)/1000 as SalesKg, sum(Quantity*InvoicePrice) as SalesVal from
#                     (select item.*,SRID, InvoiceDate from
#                     (select invoiceid, InvoiceDate , SRID from SalesInvoices where InvoiceDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
#                     and convert(varchar(10),DATEADD(D,0,GETDATE()),126)
#                     ) as Sales
#                     inner join
#                     (select invoiceid,Quantity, Weight, InvoicePrice from SalesInvoiceItem
#                     left join Hierarchy_SKU
#                     on SalesInvoiceItem.SKUID = Hierarchy_SKU.SKUID
#                     ) as item
#                     on sales.invoiceid=item.invoiceid where SRID=22) as fwe
#                     group by left(InvoiceDate, 10) """, conn)
#
# days = day_wise_sales_df.Date.tolist()
# day_salesVal = day_wise_sales_df.SalesVal.tolist()
# day_salesKg = day_wise_sales_df.SalesKg.tolist()
#
#
# cumulativeWeight = Cumulative(day_salesKg)
# cumulativeWeight = cumulativeTarget[:int(current_day)]
#
#
# cumulativeSalesVal = Cumulative(day_salesVal)
# cumulativeSalesVal = cumulativeSalesVal[:int(current_day)]


# # ------------ SR Info with brand wise sales and target -------------------------
# # -------------------------------------------------------------------------------

profile_df = pd.read_sql_query("""
            select t1.SRID,t1.SRName,t2.SRDESIGNATION, t1.ReportingBoss, t1.Brand, 
            t1.BrandName,t1.TargetVal,t2.SalesVal,T2.SalesKg, t1.TargetQty,t2.SalesQty from
            (select A.SRID, SRSNAME as SRName, ASENAME as 'ReportingBoss',
            B.Brand as Brand, BrandName, sum(TargetVal) as TargetVal , sum(TargetQty) as TargetQty
            from
            (select SRID, SRSNAME, ASENAME  from Hierarchy_EMP) as A
            left join
            (select BrandName,SRID,
            count(distinct Hierarchy_SKU.BrandID) as Brand,
            sum(TargetValue) as [TargetVal] , sum(TargetQty) as [TargetQty]
            from TargetDistributionItemBySR
            left join Hierarchy_SKU
            on TargetDistributionItemBySR.SKUID = Hierarchy_SKU.SKUID
            where [TargetQty] >0 and YearMonth=convert(varchar(6),DATEADD(MONTH, 0,getdate()), 112)
            group by SRID, ShortName,BrandName
            ) as B
            on A.SRID = B.SRID
            group by B.Brand, A.SRID, A.SRSNAME, A.ASENAME, BrandName )as T1
            left join
            (
            select a.srid,b.SRNAME,ltrim(rtrim(brandname)) as BrandName,b.SRDESIGNATION,
            SUM(Quantity) as SalesQty, sum(Quantity*InvoicePrice) as SalesVal,  SUM(Quantity*Weight)/1000 as SalesKg from
            (select item.*,SRID from
            (select * from SalesInvoices where InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
            and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126)) as Sales
            inner join
            (
            select * from SalesInvoiceItem) as item
            on sales.invoiceid=item.invoiceid) as a
                                    
            left join
            (select * from Hierarchy_SKU) as SKu
            on a.skuid=sku.skuid
            left join
            (select * from Hierarchy_Emp) as b
            on a.srid=b.srid
            group by a.srid,b.SRNAME,ltrim(rtrim(brandname)) , b.SRDESIGNATION) as T2
            on t1.SRID=t2.SRID
            and t1.BrandName=t2.BrandName
            where T2.SRID = 22
            
                           """, conn)

sr_name = profile_df.SRName.loc[0]
reporting_boss = profile_df.ReportingBoss.loc[0]
total_brand = profile_df.Brand.count()
designation = profile_df.SRDESIGNATION.loc[0]
sales_val = int(sum(profile_df.SalesVal))
sales_kg = int(sum(profile_df.SalesKg))
brand_list = profile_df.BrandName.tolist()
Sales_Val_list = profile_df['SalesVal'].tolist()
sales_kg_list = profile_df['SalesKg'].tolist()

# # -------- Trends Calculation ----------------
date = datetime.datetime.now()
current_day = int(date.strftime("%d")) - 1
days_in_month = max(monthrange(int(date.strftime("%Y")), int(date.strftime("%m"))))

mtd_avg_sales = sales_val / int(current_day)
each_day_target = total_val_target / int(days_in_month)
each_day_sales = sales_val / int(current_day)

trend_percent = round((sales_val * 100) / total_val_target, 2)
# print('Trend % = ', trend_percent)
trend_val = round((each_day_sales * days_in_month), 2)
# print('Trend Val = ', trend_val)

# # ----------- Trend Weight ---------------------------------

w_trend_per = round((sales_kg * 100 / total_weight_target), 2)
# print('Weight trend percent = ', w_trend_per)

each_day_sales_kg = sales_kg / int(current_day)
trend_val_kg = round((each_day_sales_kg * days_in_month), 2)
# print('Trend in Kg = ', trend_val_kg)

# # -------- Invoice count ----------------------------------
invoice_df = pd.read_sql_query(""" select count(InvoiceID) as TotalInvoice 
            from SalesInvoices 
            where SRID = 22 and 
            InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
            and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) """, conn)

total_invoice = int(invoice_df.TotalInvoice)
val_drop_size = int(sales_val / total_invoice)
w_drop_size = int(sales_kg / total_invoice)

# # ------------------- Strike Rate ---------------------------
total_cust_df = pd.read_sql_query(""" select count(customerid) as TotalCustomer from Customers
where routeid in (select distinct routeid from SalesInvoices where InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) and srid=22) """, conn)

total_cust = int(total_cust_df.TotalCustomer)

effective_cust_df = pd.read_sql_query(""" select count(distinct CustomerID) as EffectiveCust 
            from SalesInvoices 
            where srid=22 and InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
            and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) """, conn)

effective_cust = int(effective_cust_df.EffectiveCust)

strike_rate = round((effective_cust / total_cust) * 100, 2)
# print('Strike Rate = ', strike_rate)

# # -------------------------- Visit Rate ----------------------------------

visit_cust_df = pd.read_sql_query("""select count(distinct CustomerID) as VisitCust
                from SalesOrders 
                where srid = 22 and OrderDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) """, conn)
visited_cust = int(visit_cust_df.VisitCust)

visit_rate = round((visited_cust / total_cust) * 100, 2)
# print('Visit Rate = ', visit_rate)




# # --------- Day wise Drop size -----------------------------------
day_drop_size_df = pd.read_sql_query(""" select right(left(left(InvoiceDate, 12),6),2) as Date, SUM(SalesInvoiceItem.Quantity * SalesInvoiceItem.InvoicePrice) as Sales
                ,count(SalesInvoices.InvoiceID) as TotalInvoice, 
                (SUM(SalesInvoiceItem.Quantity * SalesInvoiceItem.InvoicePrice)/count(SalesInvoices.InvoiceID)) as DropSizeValue
                ,(sum(SalesInvoiceItem.Quantity * Weight)/1000)/count(SalesInvoices.InvoiceID) as DropSizeKg
                from SalesInvoices 
                left join SalesInvoiceItem 
                on SalesInvoices.InvoiceID = SalesInvoiceItem.InvoiceID
                                
                left join Hierarchy_SKU
                on SalesInvoiceItem.SKUID = Hierarchy_SKU.SKUID
                where SRID = 22 and 
                InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126)
                group by InvoiceDate 
                order by InvoiceDate asc """, conn)

drop_days = day_drop_size_df.Date.tolist()
drop_size_val = day_drop_size_df.DropSizeValue.tolist()
drop_size_kg = day_drop_size_df.DropSizeKg.tolist()

# print(drop_days)
# print(drop_size_val)


# # --------- Day wise strike rate --------------------------------
day_strike_df = pd.read_sql_query(""" 
                 select right(left(left(InvoiceDate, 12),6),2) as Date, 
                count(distinct SalesInvoices.CustomerID) as Effective,
                count(distinct Customers.customerid) as TotalCustomer from
                (select routeid,CustomerID
                 from Customers) as Customers
                right join 
                (select routeid,customerid,InvoiceDate from SalesInvoices
                inner join 
                 SalesInvoiceItem
                on SalesInvoices.invoiceid=SalesInvoiceItem.invoiceid
                where InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) and srid=22)
                 as SalesInvoices
                on Customers.routeid = SalesInvoices.routeid
                group by right(left(left(InvoiceDate, 12),6),2)
                """, conn)

strike_days1 =  day_strike_df.Date.tolist()
effective_strike =  day_strike_df.Effective
totalCustomer_strike =  day_strike_df.TotalCustomer
sr = ((effective_strike/totalCustomer_strike)*100).tolist()
day_strike_rate = []
for i in range(len(sr)):
    day_strike_rate.append(int(sr[i]))
# print('Strike Days = ',strike_days1)


# # ------------ Day wise Visit Rate -------------------------
day_visit_rate_df = pd.read_sql_query(""" select right(left(left(OrderDate, 12),6),2) as Date, 
                    count(distinct SalesInvoices.CustomerID) as SalesCustomer,
                    count(distinct Customers.customerid) as VisitedCustomer from
                    (select routeid,CustomerID
                    from Customers) as Customers
                    right join 
                    (select routeid,customerid,OrderDate from SalesOrders
                    inner join 
                    SalesOrderItem
                    on SalesOrders.OrderID=SalesOrderItem.OrderID
                    where OrderDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                    and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) and srid=22)
                    as SalesInvoices
                    on Customers.routeid = SalesInvoices.routeid
                    group by right(left(left(OrderDate, 12),6),2)
                    order by date asc 
                                 """, conn)

visit_days =  day_visit_rate_df.Date.tolist()
SalesCustomer =  day_visit_rate_df.SalesCustomer
VisitedCustomer =  day_visit_rate_df.VisitedCustomer
# print('visit days = ', visit_days)
vl= ((SalesCustomer/VisitedCustomer)*100).tolist()
day_visit_rate = []
for i in range(len(vl)):
    day_visit_rate.append(int(vl[i]))


# # ----------- Day wise LPS Rate ---------------------------------------
day_wise_lpc = pd.read_sql_query(""" select day(invoicedate) as Date ,count( sale.invoiceid)/count(distinct 
sale.InvoiceID) as LPC from  
                (select * from SalesInvoices where InvoiceDate  between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) and srid=22) as sale
                inner join 
                (select * from SalesInvoiceItem) as item
                on sale.invoiceid=item.invoiceid
                group by day(invoicedate)
                order by day(invoicedate) asc
                                """, conn)

lpc_days =  day_wise_lpc.Date.tolist()
lpc_rate = day_wise_lpc.LPC.tolist()
lpc = round(sum(day_wise_lpc.LPC)/len(lpc_rate), 2)


