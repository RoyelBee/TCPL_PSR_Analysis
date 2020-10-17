import matplotlib.pyplot as plt
import pandas as pd
import pyodbc


conn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=10.168.2.168;'
                      'DATABASE=TCPL_SECONDARY;'
                      'UID=sa;'
                      'PWD=erp;')

dataset = pd.read_sql_query(
"""
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
where [TargetQty] >0 and YearMonth=202009
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
x = dataset['BrandName'].tolist()
y = dataset['SalesKg'].tolist()
# con_y = dataset['SalesKg'].tolist()
# y = list(map(int, con_y))


fig, ax = plt.subplots(figsize=(6.4, 4.8))

colors = ['yellow', 'orange', 'violet', '#DADADA', '#003f5c', '#665191', '#a05195', '#d45087', '#ff7c43', '#ffa600']
bars = plt.bar(x, height=y, color=colors, width=.4)

for bar in bars:
    yval = bar.get_height()
    wval = bar.get_width()
    data = str(round(yval, 2)) + " Kg"
    plt.text(bar.get_x()+wval/16, yval * (100 / 100) + 5, data, fontweight='bold')

plt.title("Brand wise Sales in KG", fontsize=16, fontweight='bold', color='#3e0a75')
plt.xlabel('Brand', fontsize='14', color='black', fontweight='bold')
plt.ylabel('Sales',fontsize='14', color='black', fontweight='bold')


plt.rcParams['text.color'] = 'black'
plt.tight_layout()
plt.show()

