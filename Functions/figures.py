import pyodbc as db
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Functions.kpi as data

conn = db.connect('DRIVER={SQL Server};'
                  'SERVER=10.168.2.168;'
                  'DATABASE=TCPL_SECONDARY;'
                  'UID=sa;'
                  'PWD=erp;')

# df = pd.read_sql_query("""
#         select t1.SRID,t1.SRName,t1.ReportingBoss, t1.Brand, t1.BrandName,t1.TargetVal,t2.SalesVal, t1.TargetQty,t2.SalesQty from
#         (select A.SRID, SRSNAME as SRName, ASENAME as 'ReportingBoss',-- B.SKUID ,
#         --ShortName as SKUName
#         B.Brand as Brand, BrandName, sum(TargetVal) as TargetVal , sum(TargetQty) as TargetQty
#         from
#         (select SRID, SRSNAME, ASENAME  from Hierarchy_EMP) as A
#         left join
#         (select BrandName,SRID,
#          --TargetDistributionItemBySR.SKUID as SKUID , ShortName,
#           count(distinct Hierarchy_SKU.BrandID) as Brand,
#          sum(TargetValue) as [TargetVal] , sum(TargetQty) as [TargetQty]
#         from TargetDistributionItemBySR
#         left join Hierarchy_SKU
#         on TargetDistributionItemBySR.SKUID = Hierarchy_SKU.SKUID
#         where [TargetQty] >0 and YearMonth=202009
#         group by SRID, ShortName,BrandName
#         ) as B
#         on A.SRID = B.SRID
#         group by B.Brand, A.SRID, A.SRSNAME, A.ASENAME, BrandName )as T1
#         left join
#         (
#         select a.srid,b.SRNAME,ltrim(rtrim(brandname)) as BrandName,
#         SUM(Quantity) as SalesQty, sum(Quantity*InvoicePrice) as SalesVal from
#         (select item.*,SRID from
#         (select * from SalesInvoices where InvoiceDate>='1 aug 2020') as Sales
#         inner join
#         (
#         select * from SalesInvoiceItem) as item
#         on sales.invoiceid=item.invoiceid) as a
#
#         left join
#         (select * from Hierarchy_SKU) as SKu
#         on a.skuid=sku.skuid
#         left join
#         (select * from Hierarchy_Emp) as b
#         on a.srid=b.srid
#         group by a.srid,b.SRNAME,ltrim(rtrim(brandname)) ) as T2
#         on t1.SRID=t2.SRID
#         and t1.BrandName=t2.BrandName
#
#         where T2.SRID = 22
#              """, conn)
#
# print(df.columns)
# srid = df['SRID'].iloc[0]
# sr_name = df['SRName'].iloc[0]
# ReportingBoss = df['ReportingBoss'].iloc[0]
# total_brand = df['Brand'].count()
# brand_name = df['BrandName']
# target_val = df['TargetVal'].tolist()
# sales_val = df['SalesVal'].tolist()
# target_qty = df['TargetQty'].tolist()
# sales_qty = df['SalesQty'].tolist()
#
# value_achiv = round((sum(target_val) / sum(sales_val)) * 100, 2)
# qty_achiv = round((sum(target_qty) / sum(sales_qty)) * 100, 2)
#
# print(srid)
# print(sr_name)
# print(ReportingBoss)
# print(total_brand)
# print('-----------------')
# print(brand_name)
# print(target_val)
# print(sales_val)
# print(target_qty)
# print(sales_qty)
#
# print('Sales Achievements = ', str(value_achiv) + '%')
# print('Quantity Achievements = ', str(qty_achiv) + '%')

# # ---------- Cumulative Charts ---------------------------------------------
# # --------------------------------------------------------------------------

# target = data.cumulativeTarget
# sales = data.cumulativeSalesVal
#
# # sales = data.cumulativeSalesVal
# x = range(1, len(target) + 1, 1)
# xx = range(1, len(sales) + 1, 1)
#
# fig, ax = plt.subplots(figsize=(12.81, 4.8))
# plt.fill_between(x, target, color="skyblue", alpha=1)
# plt.plot(xx, sales, color="red", linewidth=5, linestyle="-")
# plt.xlabel('Days', fontsize='14', color='black', fontweight='bold')
# plt.ylabel('Amount', fontsize='14', color='black', fontweight='bold')
# # ax.set_ylabel('Amount', fontsize='14', color='black', fontweight='bold')
# # ax.set_xlabel('Day', fontsize='14', color='black', fontweight='bold')
# plt.title('01. MTD Target vs Sales in Taka - Cumulative', fontsize=16, fontweight='bold', color='#3e0a75')
# plt.xticks(np.arange(1, data.days_in_month + 1, 1))
# plt.legend(['Sales', 'Target'], loc='upper right', fontsize='14')
# # plt.show()
# plt.savefig('../Images/target_sales_val.png')


brand_sales_df = pd.read_sql_query(""" select brandname, sum(Quantity*InvoicePrice) as sales from
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
                where a.srid=22
                group by brandname""", conn)

brand_name = brand_sales_df.brandname.tolist()
brand_sales = brand_sales_df.sales.tolist()

width = 0.75
y_pos = np.arange(len(brand_name))

fig, ax = plt.subplots()
bars = plt.bar(y_pos, brand_sales, width, align='center', alpha=1)


def autolabel(bars):
    # attach some text labels
    for rect in bars:
        height = int(rect.get_height())
        ax.text(rect.get_x() + rect.get_width() / 2., .995 * height,
                height, ha='center', va='bottom', fontsize=12,  fontweight='bold')


# bars[0].set_color('#2c8e14')
# bars[1].set_color('#deff00')
# bars[2].set_color('#ff6500')
# bars[3].set_color('#f00228')

autolabel(bars)

plt.xticks(y_pos, brand_name, fontsize=12)
# plt.yticks(fontsize=12)
# plt.yticks(np.arange(0, maf_kor2 + (.6 * maf_kor2), maf_kor2 / 5), fontsize=12)
plt.xlabel('Brand Name', color='black', fontsize=14, fontweight='bold')
plt.ylabel('Amount', color='black', fontsize=14, fontweight='bold')
plt.title(' Brand Wise Sales', color='#3e0a75', fontweight='bold', fontsize=16)
plt.tight_layout()

plt.show()
# plt.savefig('aging_matured_credit.png')
# plt.close()
# print('4. Aging Mature Credit Generated')