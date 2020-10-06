import pandas as pd
import openpyxl
import pyodbc as db

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

sku_df.to_excel('../Data/sku_wise_target_sales.xlsx', index=False)
print('SKU wise target and sales data saved')

