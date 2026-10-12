# Relationship checks on the raw data
# - are keys unique?
# - do links point at real rows?
# - read only, changes nothing
import pandas as pd

# File path
# - capital letters = a value that never changes
FILE = "data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx"

# Load the four tables
suppliers = pd.read_excel(FILE, sheet_name="Suppliers")
reagents = pd.read_excel(FILE, sheet_name="Reagents")
orders = pd.read_excel(FILE, sheet_name="Purchase_Orders")
batches = pd.read_excel(FILE, sheet_name="Batch_Inventory")

# Unique keys
# - duplicated() marks repeats after the first
# - 0 means every key appears once
print("duplicate Supplier_ID:", suppliers["Supplier_ID"].duplicated().sum())
print("duplicate Reagent_ID:", reagents["Reagent_ID"].duplicated().sum())
print("duplicate PO_Number:", orders["PO_Number"].duplicated().sum())
print("duplicate Batch_ID:", batches["Batch_ID"].duplicated().sum())

# Orphan counter
# - def = a reusable block of code
# - counts child_col values with no match in parent_col
# - missing values are skipped
def orphans(child, child_col, parent, parent_col):
    values = child[child_col].dropna()
    return (~values.isin(parent[parent_col])).sum()

# Links
print("orders -> suppliers orphans:", orphans(orders, "Supplier_ID", suppliers, "Supplier_ID"))
print("orders -> reagents orphans:", orphans(orders, "Reagent_ID", reagents, "Reagent_ID"))
print("batches -> reagents orphans:", orphans(batches, "Reagent_ID", reagents, "Reagent_ID"))
