import Functions.all_functions as fn
import pandas as pd

def DayWiseDropSize(id):
    day_drop_size_df = pd.read_sql_query(""" select right(left(left(InvoiceDate, 12),6),2) as Date, SUM(SalesInvoiceItem.Quantity * SalesInvoiceItem.InvoicePrice) as Sales
                        ,count(SalesInvoices.InvoiceID) as TotalInvoice,
                        (SUM(SalesInvoiceItem.Quantity * SalesInvoiceItem.InvoicePrice)/count(SalesInvoices.InvoiceID)) as DropSizeValue
                        ,(sum(SalesInvoiceItem.Quantity * Weight)/1000)/count(SalesInvoices.InvoiceID) as DropSizeKg
                        from SalesInvoices
                        left join SalesInvoiceItem
                        on SalesInvoices.InvoiceID = SalesInvoiceItem.InvoiceID
                        left join Hierarchy_SKU
                        on SalesInvoiceItem.SKUID = Hierarchy_SKU.SKUID
                        where SRID like ? and
                        InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                        and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126)
                        group by InvoiceDate
                        order by InvoiceDate asc """, fn.conn, params={id})

    drop_days = day_drop_size_df.Date.tolist()
    drop_size_val = day_drop_size_df.DropSizeValue.tolist()
    drop_size_kg = day_drop_size_df.DropSizeKg.tolist()

    return drop_days, drop_size_val, drop_size_kg