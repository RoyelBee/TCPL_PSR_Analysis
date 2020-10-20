-------------------------- Target Value and Volume Query -------------------------
select  isnull(sum(targetvalue), 0) as TargetVal,
isnull(sum((targetqty)*Weight)/1000, 0) as TargetKg
from TargetDistributionItemBySR
left join Hierarchy_SKU
on TargetDistributionItemBySR.SKUID =Hierarchy_SKU.SKUID
where srid = '22'and yearmonth = CONVERT(VARCHAR(6),DATEADD(MONTH, 0,GETDATE()), 112)


------------------- Return Query ------------------------------------------------
select isnull(sum(Quantity*InvoicePrice),0) as ReturnVal , 
isnull(sum(Quantity*Weight)/100, 0) as ReturnKg from MarketReturns
left join
MarketReturnItem
on MarketReturns.MarketReturnID = MarketReturnItem.MarketReturnID
left join Hierarchy_SKU
on MarketReturnItem.SKUID = Hierarchy_SKU.SKUID
where SRID=22 and MarketReturnDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
and  convert(varchar(10),DATEADD(D,0,GETDATE()-1),126)


-- -----------------------------User Profiles ------------------------------------
-- PSR name, reporting boss, brands, target, sales, quantity wise target and sales 
----------------------------------------------------------------------------------

select t1.SRID,t1.SRName,t2.SRDESIGNATION, t1.ReportingBoss, t1.Brand, 
t1.BrandName,t1.TargetVal, t1.TargetKG, t2.SalesVal,T2.SalesKg, t1.TargetQty,t2.SalesQty from
(select A.SRID, SRSNAME as SRName, ASENAME as 'ReportingBoss',
B.Brand as Brand, BrandName, sum(TargetVal) as TargetVal , sum(TargetQty) as TargetQty, sum(TargetQty*Tweight)/1000 as TargetKG
from
(select SRID, SRSNAME, ASENAME  from Hierarchy_EMP) as A
left join
(select BrandName,SRID,weight as Tweight,
count(distinct Hierarchy_SKU.BrandID) as Brand,
sum(TargetValue) as [TargetVal] , sum(TargetQty) as [TargetQty]
from TargetDistributionItemBySR
left join Hierarchy_SKU
on TargetDistributionItemBySR.SKUID = Hierarchy_SKU.SKUID
where [TargetQty] >0 and YearMonth=convert(varchar(6),DATEADD(MONTH, 0,getdate()), 112)
group by SRID, ShortName,BrandName,weight
) as B
on A.SRID = B.SRID
group by B.Brand, A.SRID, A.SRSNAME, A.ASENAME, BrandName )as T1
left join
(
select a.srid,b.SRNAME,ltrim(rtrim(brandname)) as BrandName,b.SRDESIGNATION,
SUM(Quantity) as SalesQty, sum(Quantity*InvoicePrice) as SalesVal,  SUM(Quantity*Weight)/1000 as SalesKg from
(select item.*,SRID from
(select * from SalesInvoices where InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126)) as Sales
inner join
(
select * from SalesInvoiceItem) as item
on sales.invoiceid=item.invoiceid) as a

left join
(select * from Hierarchy_SKU) as SKu
on a.skuid=sku.skuid
left join
(select * from Hierarchy_Emp) as b
on a.srid=b.srid
group by a.srid,b.SRNAME,ltrim(rtrim(brandname)) , b.SRDESIGNATION) as T2
on t1.SRID=t2.SRID
and t1.BrandName=t2.BrandName
where T2.SRID = 22


-------------------------- Invoice Information -------------------------------------
select count(InvoiceID) as TotalInvoice 
from SalesInvoices 
where SRID = 22 and 
InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126)


----------------------------- Total Customer ---------------------------------------
select count(customerid) as TotalCustomer from Customers
where routeid in (select distinct routeid from SalesInvoices 
where InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) and srid=22)


--------------- --------Effective Customer (Actual Sales made customer)-------------
select count(distinct CustomerID) as EffectiveCust 
from SalesInvoices 
where srid=22 and InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126)

---------------------------- Visited Customer --------------------------------------
select count(distinct CustomerID) as VisitCust
from SalesOrders 
where srid = 22 and OrderDate between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126)


---------------------------- Day wise drop size ------------------------------------
select right(left(left(InvoiceDate, 12),6),2) as Date, SUM(SalesInvoiceItem.Quantity * SalesInvoiceItem.InvoicePrice) as Sales
,count(SalesInvoices.InvoiceID) as TotalInvoice, 
(SUM(SalesInvoiceItem.Quantity * SalesInvoiceItem.InvoicePrice)/count(SalesInvoices.InvoiceID)) as DropSizeValue
,(sum(SalesInvoiceItem.Quantity * Weight)/1000)/count(SalesInvoices.InvoiceID) as DropSizeKg
from SalesInvoices 
left join SalesInvoiceItem 
on SalesInvoices.InvoiceID = SalesInvoiceItem.InvoiceID

left join Hierarchy_SKU
on SalesInvoiceItem.SKUID = Hierarchy_SKU.SKUID
where SRID = 22 and 
InvoiceDate between  convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126)
group by InvoiceDate 
order by InvoiceDate asc


------------------------- Day wise Strike rate -----------------------------------
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
and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) and srid=22)
as SalesInvoices
on Customers.routeid = SalesInvoices.routeid
group by right(left(left(InvoiceDate, 12),6),2)



---------------------- Day wise visit rate -------------------------------------
select right(left(left(OrderDate, 12),6),2) as Date, 
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
and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) and srid=22)
as SalesInvoices
on Customers.routeid = SalesInvoices.routeid
group by right(left(left(OrderDate, 12),6),2)
order by date asc 


----------------------- Day wise LPC ------------------------------------------
select day(invoicedate) as Date ,count( sale.invoiceid)/count(distinct 
sale.InvoiceID) as LPC from  
(select * from SalesInvoices where InvoiceDate  between convert(varchar(10),DATEADD(mm, DATEDIFF(mm, 0, GETDATE()), 0),126)
and convert(varchar(10),DATEADD(D,0,GETDATE()-1),126) and srid=22) as sale
inner join 
(select * from SalesInvoiceItem) as item
on sale.invoiceid=item.invoiceid
group by day(invoicedate)
order by day(invoicedate) asc


---------------------------- SKU wise Sales ----------------------------------
DECLARE @date date = GETDATE(); 
declare @current_day int = right(convert(varchar(8),getdate()-1, 112), 2)

select cast(item.skuid as int) as SKUID,
item.ShortName as [SKU Name],
cast(isnull(sum(targetv.TargetValue), 0) as int) as [Months Sales Target(Tk)],
cast((sum(targetv.TargetValue) /  cast(DAY(EOMONTH ( @date )) as int)) * @current_day as int) as [MTD Sales Target(Tk)],

cast(isnull(sum(Quantity*InvoicePrice), 0) as int) as [MTD Sales(Tk)],
(sum(Quantity*InvoicePrice) /((sum(targetv.TargetValue) /  cast(DAY(EOMONTH ( @date )) as int)) * @current_day ))*100 as [Value Achiv %] , 

cast(isnull(sum(targetv.TargetQty*Quantity)/1000, 0) as int) as [Months Volume Target(Kg)],
cast((((sum(targetv.TargetQty*Quantity)/1000)/ cast(DAY(EOMONTH ( @date )) as int)) * @current_day) as int) as [MTD Volume Target(Kg)],

cast(isnull(sum(Quantity*Weight)/1000, 0) as int) as [Sales Volume(Kg)], 
((sum(Quantity*Weight)/1000)/(((sum(targetv.TargetQty*Quantity)/1000)/ cast(DAY(EOMONTH ( @date )) as int)) * @current_day))*100 as [Volume Achiv %]
from

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

where item.skuid> 0
group by item.skuid, item.ShortName
--order by [Sales Value] desc