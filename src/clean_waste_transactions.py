# Waste_Transactions cleaning (decision D11)
# - reads the raw sheet, saves a cleaned Parquet file
import pandas as pd

# File path
FILE = "data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx"

# Load both sheets
# - Reagents supplies the cost per unit
waste = pd.read_excel(FILE, sheet_name="Waste_Transactions")
reagents = pd.read_excel(FILE, sheet_name="Reagents")

# Work on a copy
# - original waste table stays untouched
cleaned = waste.copy()

# D11: waste cost
# - keep the recorded cost in Waste_Cost_Original_ZAR
# - add each reagent's cost per unit
# - Waste_Cost_ZAR = Quantity_Wasted x Cost_Per_Unit_ZAR
# - drop the helper column afterwards
cleaned["Waste_Cost_Original_ZAR"] = cleaned["Waste_Cost_ZAR"]
cleaned = cleaned.merge(reagents[["Reagent_ID", "Cost_Per_Unit_ZAR"]], on="Reagent_ID", how="left")
cleaned["Waste_Cost_ZAR"] = cleaned["Quantity_Wasted"] * cleaned["Cost_Per_Unit_ZAR"]
cleaned = cleaned.drop(columns="Cost_Per_Unit_ZAR")

# Save
# - write to data/processed as Parquet
cleaned.to_parquet("data/processed/waste_transactions.parquet", index=False)

# Read it back and report
# - shape, types, missing values
# - total of each cost column
check = pd.read_parquet("data/processed/waste_transactions.parquet")
print(check.shape)
print(check.dtypes)
print("missing values:", check.isna().sum().sum())
print("total recorded cost:", check["Waste_Cost_Original_ZAR"].sum())
print("total calculated cost:", check["Waste_Cost_ZAR"].sum())