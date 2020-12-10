import pandas as pd
import Functions.all_functions as fn


def TotalTarget(id):
    target_df = pd.read_sql_query(""" select  isnull(sum(targetvalue), 0) as TargetVal,
                    isnull(sum((targetqty)*Weight)/1000, 0) as TargetKg
                    from TargetDistributionItemBySR
                    left join Hierarchy_SKU
                    on TargetDistributionItemBySR.SKUID = Hierarchy_SKU.SKUID
                    where srid like ? and yearmonth = CONVERT(VARCHAR(6),DATEADD(MONTH, 0,GETDATE()), 112)
                    """, fn.conn, params={id})

    return int(target_df.TargetVal), int(target_df.TargetKg)
