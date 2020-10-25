import pandas as pd
import pyodbc as db

conn = db.connect('DRIVER={SQL Server};'
                  'SERVER=10.168.2.168;'
                  'DATABASE=TCPL_SECONDARY;'
                  'UID=sa;'
                  'PWD=erp;')

sr_df = pd.read_sql_query(""" select  Hierarchy_Emp.srid, SRNAME from Hierarchy_Emp
        left join SalesInvoices 
        on Hierarchy_Emp.SRID=SalesInvoices.SRID
        
        where InvoiceDate = convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
        group by Hierarchy_Emp.srid, SRNAME
        order by Hierarchy_Emp.srid asc """, conn)

# print(id)

## [22, 23, 25, 26, 28, 30, 31, 40, 41, 42, 43, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 62, 63, 64, 65,
# 73, 92, 93, 94, 95, 97, 98, 99, 100, 101, 102, 104, 105, 106, 107, 108, 109, 111, 113, 114, 115, 116, 117, 118, 119,
# 120, 121, 122, 127, 130, 132, 138]
import math

id = sr_df.srid.tolist()

j = 0
k = 10
lenth = math.ceil(len(id) / 10)
new_list = []
for i in range(lenth):
    x = slice(j, k, 1)
    new_list.append(id[x])
    j = j + 10
    k = k + 10
# print("New list: ", new_list)

print(new_list[0])