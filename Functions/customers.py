import Functions.all_functions as fn
import pandas as pd

def TotalCust(id):
    total_cust_df = pd.read_sql_query(""" select count(customerid) as TotalCustomer from Customers
                        where routeid in (select distinct routeid from SalesInvoices
                         where InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                        and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) and SRID like ?) """, fn.conn, params={id})

    return int(total_cust_df.TotalCustomer)

def EffectiveCust(id):
    effective_cust_df = pd.read_sql_query(""" select count(distinct CustomerID) as EffectiveCust  from
                        (select * from SalesInvoices
                        where SRID like ? and InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                        and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126)) as sale
                        inner  join
                        (select * from SalesInvoiceItem) as item
                        on sale.invoiceid=item.invoiceid """, fn.conn, params={id})

    return int(effective_cust_df.EffectiveCust)

def VisitCust(id):
    visit_cust_df = pd.read_sql_query(""" select count(distinct CustomerID) as VisitCust
                        from SalesOrders
                        where srid like ? and OrderDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),
                        126)
                        and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) """, fn.conn, params={id})
    return int(visit_cust_df.VisitCust)
