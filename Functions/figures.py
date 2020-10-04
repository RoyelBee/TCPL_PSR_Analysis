import pyodbc as db
import pandas as pd
import matplotlib.pyplot as plt

skf_conn = db.connect('DRIVER={SQL Server};'
                      'SERVER=137.116.139.217;'
                      'DATABASE=ARCHIVESKF;'
                      'UID=sa;PWD=erp@123')
conn = db.connect('DRIVER={SQL Server};'
                  'SERVER=10.168.2.168;'
                  'DATABASE=TCPL_SECONDARY;'
                  'UID=sa;'
                  'PWD=erp;')

df = pd.read_sql_query("""
        select t1.SRID,t1.SRName,t1.ReportingBoss, t1.Brand, t1.BrandName,t1.TargetVal,t2.SalesVal, t1.TargetQty,t2.SalesQty from 
        (select A.SRID, SRSNAME as SRName, ASENAME as 'ReportingBoss',-- B.SKUID ,
        --ShortName as SKUName
        B.Brand as Brand, BrandName, sum(TargetVal) as TargetVal , sum(TargetQty) as TargetQty
        from
        (select SRID, SRSNAME, ASENAME  from Hierarchy_EMP) as A
        left join
        (select BrandName,SRID,
         --TargetDistributionItemBySR.SKUID as SKUID , ShortName, 
          count(distinct Hierarchy_SKU.BrandID) as Brand,
         sum(TargetValue) as [TargetVal] , sum(TargetQty) as [TargetQty] 
        from TargetDistributionItemBySR
        left join Hierarchy_SKU
        on TargetDistributionItemBySR.SKUID = Hierarchy_SKU.SKUID
        where [TargetQty] >0 and YearMonth=202009
        group by SRID, ShortName,BrandName
        ) as B
        on A.SRID = B.SRID
        group by B.Brand, A.SRID, A.SRSNAME, A.ASENAME, BrandName )as T1
        left join 
        (
        select a.srid,b.SRNAME,ltrim(rtrim(brandname)) as BrandName, 
        SUM(Quantity) as SalesQty, sum(Quantity*InvoicePrice) as SalesVal from 
        (select item.*,SRID from 
        (select * from SalesInvoices where InvoiceDate>='1 aug 2020') as Sales
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
        group by a.srid,b.SRNAME,ltrim(rtrim(brandname)) ) as T2
        on t1.SRID=t2.SRID
        and t1.BrandName=t2.BrandName
        
        where T2.SRID = 22
             """, conn)

print(df.columns)
srid = df['SRID'].iloc[0]
sr_name = df['SRName'].iloc[0]
ReportingBoss = df['ReportingBoss'].iloc[0]
total_brand = df['Brand'].count()
brand_name = df['BrandName']
target_val = df['TargetVal'].tolist()
sales_val = df['SalesVal'].tolist()
target_qty = df['TargetQty'].tolist()
sales_qty = df['SalesQty'].tolist()

value_achiv = round((sum(target_val) / sum(sales_val)) * 100, 2)
qty_achiv = round((sum(target_qty) / sum(sales_qty)) * 100, 2)

print(srid)
print(sr_name)
print(ReportingBoss)
print(total_brand)
print('-----------------')
print(brand_name)
print(target_val)
print(sales_val)
print(target_qty)
print(sales_qty)

print('Sales Achievements = ', str(value_achiv) + '%')
print('Quantity Achievements = ', str(qty_achiv) + '%')
