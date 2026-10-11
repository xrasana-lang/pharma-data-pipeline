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
- Verified: with slash dates read as day/month/year, the gap between Order_Date and Expected_Delivery_Date is 5 to 45 days (average about 25) in all 4000 rows, with 0 negative gaps

## D4: Bad Expiry_Date in Batch_Inventory
- Finding: 14 of 6000 batches have an Expiry_Date 5 days before their Manufacture_Date
- Evidence: all 14 have a life of -5 days, spread across statuses: 7 Expired, 3 Active, 3 Consumed, 1 Disposed
- Not repairable: only 1932 of 6000 batches have a life equal to the reagent's Shelf_Life_Days, and the rest differ by whole years, so the correct date cannot be worked out
- Decision: keep the 14 rows, set Expiry_Date to missing, and add a flag column marking them
- Reason: keeps the batch records without letting a wrong date into any calculation
- Open: Current_Status does not seem to follow Expiry_Date, because Expired and Active batches have overlapping expiry ranges. Not resolved yet

## D6: Storage_Type and Temperature_Range do not match in Storage_Locations
- Finding: Storage_Type and Temperature_Range look unrelated. Only 6 of 16 Freezers are at -20C, and only 1 of 9 Refrigerators is at 2-8C. Ambient locations include -20C (5) and 2-8C (5)
- Checked: all 5884 storage codes in Batch_Inventory exist in Storage_Locations, there are no duplicate IDs, and all 50 locations are used
- Status: documented, not fixed
- Rule: leave both columns unchanged and do not use Temperature_Range for storage checks until its meaning is confirmed

