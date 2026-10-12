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
- - Finding: the Data_Dictionary sheet has one generic line per sheet and does not define Country, so the meaning of the column is undocumented
- Domain note: a supplier record normally holds the country where the supplier is registered or ships from. One supplier name under five countries suggests Country may record something else, such as the shipping origin, and needs confirming with Procurement
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
- Domain note: refrigerated storage is normally 2-8C, frozen about -20C and ambient about 15-25C, so a Freezer at 2-8C is not a consistent combination. QA or facilities should confirm which column is correct
- Checked: all 5884 storage codes in Batch_Inventory exist in Storage_Locations, there are no duplicate IDs, and all 50 locations are used
- Status: documented, not fixed
- Rule: leave both columns unchanged and do not use Temperature_Range for storage checks until its meaning is confirmed

## D5: Missing Lot_Number and Storage_Location in Batch_Inventory
- Finding: 100 of 6000 batches have no Lot_Number, and 116 have no Storage_Location. Only 2 rows are missing both, so the gaps look unrelated
- Evidence: the gaps are spread across all four statuses with no clear pattern
- Decision: fill missing Lot_Number with "Unknown", and leave missing Storage_Location as a true missing value
- Reason: Lot_Number is only a label, while Storage_Location links to the Storage_Locations table and a placeholder code would find no match in a join
- Note: D4 also applies to this table, so the 14 rows with a bad Expiry_Date keep their gap and get a flag

## D7: Missing Hazard_Class in Reagents
- Finding: 82 of 250 reagents have no Hazard_Class. No other Reagents column has gaps
- Decision: fill missing Hazard_Class with "Unknown"
- Reason: Hazard_Class is a plain label that, as far as we have seen, no other table links to, so a placeholder cannot break a join. An explicit Unknown keeps these reagents visible in any breakdown by hazard class and cannot be mistaken for "not hazardous"

## D8: Some Hazard_Class labels look implausible (DOCUMENTED, NOT FIXED)
- - Finding: some labels do not match the usual classification. REA0004 Acetonitrile HPLC Grade is labelled Corrosive, but acetonitrile is normally classified as a flammable liquid. REA0003 Paracetamol Reference Standard is labelled Flammable, but paracetamol is a solid with no flammable classification. Only the first 5 rows were looked at, so this is not checked across the table
- Status: documented, not fixed
- - Rule: leave existing labels unchanged. The project has no authoritative source, such as a safety data sheet, to correct them against. The safety officer should confirm them

## D10: Cross-table links do not agree on dates or reagents (DOCUMENTED, NOT FIXED)
- Finding: in a test join with order numbers repaired by row position, 1992 of 4000 receipts are dated before their order, and the gap ranges from -1067 to 1078 days
- Domain note: a goods receipt cannot be dated before the order it fulfils, so these dates or links need confirming with Procurement
- Finding: a batch's Reagent_ID equals the Reagent_ID of its order in only 24 of 5961 cases (0.4%), no better than a random match across 250 reagents
- Domain note: a batch received against an order should be the reagent that was ordered, so the receipt-to-order link looks unreliable
- Checked: the keys themselves link cleanly. Every batch has a receipt, every order's supplier and reagent exists, and every batch's reagent exists
- Status: documented, not fixed
- Rule: do not use order-to-receipt date gaps or the batch-to-order reagent link in analysis. Use the key links only


