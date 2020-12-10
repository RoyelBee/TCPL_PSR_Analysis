import Functions.all_functions as fn
import pandas as pd

def DayWiseLPC(id):
    day_wise_lpc = pd.read_sql_query(""" select day(invoicedate) as Date ,count( sale.invoiceid)/count(distinct
        sale.InvoiceID) as LPC from
                        (select * from SalesInvoices where InvoiceDate  between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                        and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) and SRID like ?) as sale
                        inner join
                        (select * from SalesInvoiceItem) as item
                        on sale.invoiceid=item.invoiceid
                        group by day(invoicedate)
                        order by day(invoicedate) asc
                                        """, fn.conn, params={id})

    lpc_days = day_wise_lpc.Date.tolist()
    lpc_rate = day_wise_lpc.LPC.tolist()

    return lpc_days, lpc_rate
