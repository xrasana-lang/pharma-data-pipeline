# PO_Number sequence test
# - hypothesis: PO_Number is "PO" + row position (from 1), padded to 6 digits
# - read only, changes nothing
import pandas as pd

# File path
FILE = "data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx"

# Load the sheet
df = pd.read_excel(FILE, sheet_name="Purchase_Orders")

# Expected number for each row
# - position starts at 1
# - zfill(6) pads with zeros, so 7 becomes 000007
positions = pd.Series(df.index + 1)
expected = "PO" + positions.astype(str).str.zfill(6)

# Rows where the number does not match its position
mismatch = df["PO_Number"] != expected
print("rows not matching position:", mismatch.sum())
bad = df[mismatch].copy()
bad["expected"] = expected[mismatch]
print(bad[["PO_Number", "expected"]].to_string())

# Numbers in the sequence that no row uses
missing = set(expected) - set(df["PO_Number"])
print("numbers in sequence but unused:", len(missing))
print(sorted(missing))

# First look at Goods_Receipts
receipts = pd.read_excel(FILE, sheet_name="Goods_Receipts")
print(receipts.shape)
print(receipts.columns)
print(receipts.head().to_string())
