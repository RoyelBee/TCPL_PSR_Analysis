import Functions.all_functions as fn
import pandas as pd

def StrikeDays(id):
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
                        and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) and SRID like ?)
                         as SalesInvoices
                        on Customers.routeid = SalesInvoices.routeid
                        group by right(left(left(InvoiceDate, 12),6),2)
                        """, fn.conn, params={id})

    strike_days = day_strike_df.Date.tolist()
    effective_strike = day_strike_df.Effective
    totalCustomer_strike = day_strike_df.TotalCustomer

    return strike_days, effective_strike, totalCustomer_strike