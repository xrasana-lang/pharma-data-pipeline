# Duplicate PO_Number rows in Purchase_Orders
# - read only, changes nothing
import pandas as pd

# Load the sheet
# - run from project root (relative path)
df = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Purchase_Orders")

# Rows that share a PO_Number
# - keep=False marks every row in a repeated group, including the first
# - sort so the matching rows sit next to each other
dupes = df[df["PO_Number"].duplicated(keep=False)].sort_values("PO_Number")
print("rows sharing a PO_Number:", len(dupes))
print("different PO_Numbers repeated:", dupes["PO_Number"].nunique())
print(dupes.to_string())

# Exact copies
# - rows identical in every column to an earlier row
print("exact repeat rows:", df.duplicated().sum())
