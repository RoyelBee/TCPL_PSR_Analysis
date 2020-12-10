import Functions.all_functions as fn
import pandas as pd

def VisitRate(id):
    day_visit_rate_df = pd.read_sql_query(""" select right(left(left(OrderDate, 12),6),2) as Date,
                            count(distinct SalesInvoices.CustomerID) as SalesCustomer,
                            count(distinct Customers.customerid) as VisitedCustomer from
                            (select routeid,CustomerID
                            from Customers) as Customers
                            right join
                            (select routeid,customerid,OrderDate from SalesOrders
                            inner join
                            SalesOrderItem
                            on SalesOrders.OrderID=SalesOrderItem.OrderID
                            where OrderDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                            and convert(varchar(10),DATEADD(D,0,GETDATE()),126) and SRID like ?)
                            as SalesInvoices
                            on Customers.routeid = SalesInvoices.routeid
                            group by right(left(left(OrderDate, 12),6),2)
                            order by date asc """, fn.conn, params={id})

    visit_days = day_visit_rate_df.Date.tolist()
    SalesCustomer = day_visit_rate_df.SalesCustomer
    VisitedCustomer = day_visit_rate_df.VisitedCustomer

    return visit_days, SalesCustomer, VisitedCustomer
