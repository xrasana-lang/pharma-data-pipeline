# Reagent chain test: batch -> receipt -> order
# - does Batch_Inventory.Reagent_ID agree with Purchase_Orders.Reagent_ID?
# - read only, changes nothing
import pandas as pd

# File path
FILE = "data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx"

# Load the three tables
orders = pd.read_excel(FILE, sheet_name="Purchase_Orders")
receipts = pd.read_excel(FILE, sheet_name="Goods_Receipts")
batches = pd.read_excel(FILE, sheet_name="Batch_Inventory")

# Order number by row position (the repair under test)
orders["PO_Fixed"] = "PO" + pd.Series(orders.index + 1).astype(str).str.zfill(6)

# Batch -> receipt -> PO number
chain = batches[["Batch_ID", "Receipt_ID", "Reagent_ID"]].merge(
    receipts[["Receipt_ID", "PO_Number"]], on="Receipt_ID", how="left"
)
print("batches with no receipt:", chain["PO_Number"].isna().sum())

# Part 1: normal orders
# - PO_Number appears once in the raw orders
# - how often does the batch reagent equal the order reagent?
counts = orders["PO_Number"].value_counts()
single = set(counts[counts == 1].index)
normal = orders[orders["PO_Number"].isin(single)][["PO_Number", "Reagent_ID"]]
normal = normal.rename(columns={"Reagent_ID": "Order_Reagent"})
test1 = chain.merge(normal, on="PO_Number", how="inner")
print("PART 1 batches on normal orders:", len(test1))
print("PART 1 reagent matches:", (test1["Reagent_ID"] == test1["Order_Reagent"]).sum())

# Part 2: the 17 unused numbers
# - unused = numbers in the position sequence that no order carries
# - compare the batch reagent with the reagent of the order at that position
unused = set(orders["PO_Fixed"]) - set(orders["PO_Number"])
fixed = orders[orders["PO_Fixed"].isin(unused)][["PO_Fixed", "Reagent_ID"]]
fixed = fixed.rename(columns={"PO_Fixed": "PO_Number", "Reagent_ID": "Order_Reagent"})
test2 = chain.merge(fixed, on="PO_Number", how="inner")
print("PART 2 batches on the 17 unused numbers:", len(test2))
print("PART 2 reagent matches:", (test2["Reagent_ID"] == test2["Order_Reagent"]).sum())

# Part 3: PO000123
# - batches whose receipt says PO000123
# - the 18 orders that carry that number
print("PART 3 batches on PO000123")
print(chain[chain["PO_Number"] == "PO000123"].to_string())
print("PART 3 orders carrying PO000123")
print(orders[orders["PO_Number"] == "PO000123"][["PO_Fixed", "Reagent_ID"]].to_string())
