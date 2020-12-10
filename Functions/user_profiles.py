import Functions.all_functions as fn
import pandas as pd

def UserProfile(id):
    profile_df = pd.read_sql_query("""
                select t1.SRID,t1.SRName,t2.SRDESIGNATION, t1.ReportingBoss, t1.Brand,
                t1.BrandName,t1.TargetVal, t1.TargetKG, t2.SalesVal,T2.SalesKg, t1.TargetQty,t2.SalesQty from
                (select A.SRID, SRSNAME as SRName, ASENAME as 'ReportingBoss',
                B.Brand as Brand, BrandName, sum(TargetVal) as TargetVal , sum(TargetQty) as TargetQty,
                sum(TargetQty*Tweight)/1000 as TargetKG
                from
                (select SRID, SRSNAME, ASENAME  from Hierarchy_EMP) as A
                left join
                (select BrandName,SRID,weight as Tweight,
                count(distinct Hierarchy_SKU.BrandID) as Brand,
                sum(TargetValue) as [TargetVal] , sum(TargetQty) as [TargetQty]
                from TargetDistributionItemBySR
                left join Hierarchy_SKU
                on TargetDistributionItemBySR.SKUID = Hierarchy_SKU.SKUID
                where [TargetQty] >0 and YearMonth=convert(varchar(6),DATEADD(MONTH, 0,getdate()), 112)
                group by SRID, ShortName,BrandName,weight
                ) as B
                on A.SRID = B.SRID
                group by B.Brand, A.SRID, A.SRSNAME, A.ASENAME, BrandName )as T1
                left join
                (
                select a.srid,b.SRNAME,ltrim(rtrim(brandname)) as BrandName,b.SRDESIGNATION,
                SUM(Quantity) as SalesQty, sum(Quantity*InvoicePrice) as SalesVal,  SUM(Quantity*Weight)/1000 as SalesKg from
                (select item.*,SRID from
                (select * from SalesInvoices where InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                and convert(varchar(10),DATEADD(D,0,GETDATE()-2),126)) as Sales
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
                where T2.SRID like ?

                    """, fn.conn, params={id})

    sr_name = profile_df.SRName.loc[0]
    reporting_boss = profile_df.ReportingBoss.loc[0]
    total_brand = profile_df.Brand.count()
    designation = profile_df.SRDESIGNATION.loc[0]
    sales_val_list = profile_df.SalesVal.tolist()
    sales_kg = int(sum(profile_df.SalesKg))
    brand_list = profile_df.BrandName.tolist()
    target_list = profile_df.TargetVal.tolist()
    target_kg_list = profile_df.TargetKG.tolist()

    return sr_name, reporting_boss, total_brand, designation, sales_val_list, sales_kg, brand_list, target_list, target_kg_list
