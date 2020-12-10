import Functions.all_functions as fn
import pandas as pd

def Total_Invoice(id):
    invoice_df = pd.read_sql_query(""" select count(InvoiceID) as TotalInvoice
                from SalesInvoices
                where SRID like ? and
                InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) """, fn.conn, params={id})

    return int(invoice_df.TotalInvoice)
