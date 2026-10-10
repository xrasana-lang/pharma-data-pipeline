# Data decisions

## D1: Standardise Merck supplier names
- Table: Suppliers, column Supplier_Name
- Finding: three spellings of one supplier: Merck (8 rows), Merck SA (6 rows), MERCK (3 rows), 17 of 30 rows in total
- Decision: rename all three to "Merck"
- Reason: Merck is the most common spelling, and the supplier is assumed to be local
- Rows are renamed, not removed, and each row keeps its own Supplier_ID

## D2: Supplier_ID and Country look inconsistent (DOCUMENTED, NOT FIXED)
- Finding: the 17 Merck rows have 17 different Supplier_IDs and 5 different countries
- Only 5 of the 17 are in South Africa, which does not fit the assumption that the supplier is local
- Status: documented, not fixed
- Finding: Data_Dictionary only has one generic line per sheet and does not define Country. The workbook says the data is synthetic with embedded quality issues
- Rule: leave Country unchanged and do not use it in analysis until its meaning is confirmed

## D3: Standardise Order_Date in Purchase_Orders
- Finding: Order_Date is text with three formats: 2025-02-12 (1385 rows), 02/02/2024 (1340 rows), 01-May-2025 (1275 rows), 4000 rows in total
- Evidence for slash dates: first number above 12 in 823 rows, second number above 12 in 0 rows
- Decision: read slash dates as day/month/year, then convert all of Order_Date to a real date type
- Assumption: all slash dates follow the same day/month/year order, including the 517 where both numbers are 12 or below
- Check later: Order_Date should come before Expected_Delivery_Date