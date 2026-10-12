# Goods_Receipts checks against Purchase_Orders
# - do receipts use the "missing" numbers?
# - read only, changes nothing
import pandas as pd

# File path
FILE = "data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx"

# Load both tables
orders = pd.read_excel(FILE, sheet_name="Purchase_Orders")
receipts = pd.read_excel(FILE, sheet_name="Goods_Receipts")

# The 17 numbers no order uses
# - same method as the sequence test
expected = "PO" + pd.Series(orders.index + 1).astype(str).str.zfill(6)
unused = set(expected) - set(orders["PO_Number"])

# Receipt table health
# - duplicate keys
# - how many receipts per order number
print("duplicate Receipt_ID:", receipts["Receipt_ID"].duplicated().sum())
print("duplicate PO_Number in receipts:", receipts["PO_Number"].duplicated().sum())
print("receipts for PO000123:", (receipts["PO_Number"] == "PO000123").sum())

# Do receipts use the unused numbers?
# - isin() checks membership in the set of 17
print("receipts using an unused number:", receipts["PO_Number"].isin(unused).sum())

# Orphans
# - receipt numbers with no matching order
print("receipts with no order:", (~receipts["PO_Number"].isin(orders["PO_Number"])).sum())

# Orders with no receipt
print("orders with no receipt:", (~orders["PO_Number"].isin(receipts["PO_Number"])).sum())
