SELECT DWH_GSS_CASE.CASENUMBER, DWH_GSS_CASE.EA_NAME__C, DWH_GSS_CASE.DESCRIPTION, CREATEDDATE, DWH_GSS_CASE.LASTMODIFIEDDATE, DWH_GSS_CASE.GSS_LAST_TOUCH_TIME__C, DWH_GSS_CASE.CLOSEDDATE
FROM DWH_GSS_CASE  
WHERE (PRODUCTID in (SELECT id FROM DWH_GSS_PRODUCT where NAME LIKE '%SAN%' and NAME NOT like '%Beta%') or SUBJECT like '%VSAN%')
and SUBJECT not like '%eForm%' and
GSS_PROBLEM_CATEGORY__C not in ('Licensing','Invoice','Renewals','Refund/Rebate','Registration') {0}