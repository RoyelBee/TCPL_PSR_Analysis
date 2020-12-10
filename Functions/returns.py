import Functions.all_functions as fn
import pandas as pd

def TotalReturn(id):
    return_df = pd.read_sql_query(""" select isnull(sum(Quantity*InvoicePrice),0) as ReturnVal ,
                    isnull(sum(Quantity*Weight)/100, 0) as ReturnKg from MarketReturns
                    left join
                    MarketReturnItem
                    on MarketReturns.MarketReturnID = MarketReturnItem.MarketReturnID
                    left join Hierarchy_SKU
                    on MarketReturnItem.SKUID = Hierarchy_SKU.SKUID
                    where SRID like ? and MarketReturnDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
                    and  convert(varchar(10),DATEADD(D,0,GETDATE()-1),126)
                                            """, fn.conn, params={id})

    total_val_return = sum(return_df.ReturnVal)
    total_weight_return = sum(return_df.ReturnKg)

    return total_val_return, total_weight_return
