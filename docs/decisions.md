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