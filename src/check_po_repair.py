# Test the PO_Number repair against Goods_Receipts
# - repair = number each order by its row position
# - if the repair is right, receipts join cleanly and arrive after the order
# - read only, changes nothing
import pandas as pd

# Load the cleaned orders and the raw receipts
# - orders keep the raw row order, with Order_Date already parsed
orders = pd.read_parquet("data/processed/purchase_orders.parquet")
receipts = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Goods_Receipts")
receipts["Actual_Receipt_Date"] = pd.to_datetime(receipts["Actual_Receipt_Date"])

# Repaired order numbers
# - expected = "PO" + row position, padded to 6 digits
# - unused = the 17 numbers no order has
expected = "PO" + pd.Series(orders.index + 1).astype(str).str.zfill(6)
unused = set(expected) - set(orders["PO_Number"])
repaired = orders.copy()
repaired["PO_Number"] = expected
print("repaired numbers unique:", repaired["PO_Number"].is_unique)

# Join receipts to the repaired orders
# - how="left" keeps every receipt
joined = receipts.merge(repaired[["PO_Number", "Order_Date"]], on="PO_Number", how="left")
print("receipts:", len(receipts), "rows after join:", len(joined))
print("receipts with no order after repair:", joined["Order_Date"].isna().sum())

# Days from order to receipt
# - negative means the receipt came before the order
joined["days"] = (joined["Actual_Receipt_Date"] - joined["Order_Date"]).dt.days
print("ALL receipts")
print(joined["days"].describe())
print("negative days:", (joined["days"] < 0).sum())

# Only the receipts on repaired orders
on_repaired = joined[joined["PO_Number"].isin(unused)]
print("RECEIPTS ON REPAIRED ORDERS")
print("count:", len(on_repaired))
print(on_repaired["days"].describe())
print("negative days:", (on_repaired["days"] < 0).sum())
