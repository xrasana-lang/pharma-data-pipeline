# Waste cost test
# - domain rule: cost = quantity wasted x reagent cost per unit
# - read only, changes nothing
import pandas as pd

# File path
FILE = "data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx"

# Load both tables
waste = pd.read_excel(FILE, sheet_name="Waste_Transactions")
reagents = pd.read_excel(FILE, sheet_name="Reagents")

# Add each reagent's unit cost to its waste rows
# - how="left" keeps every waste row
merged = waste.merge(reagents[["Reagent_ID", "Cost_Per_Unit_ZAR"]], on="Reagent_ID", how="left")
print("rows:", len(waste), "after join:", len(merged))
print("waste rows with no reagent:", merged["Cost_Per_Unit_ZAR"].isna().sum())

# Expected cost under the rule
merged["expected_cost"] = merged["Quantity_Wasted"] * merged["Cost_Per_Unit_ZAR"]
print("recorded cost equals expected:", (merged["Waste_Cost_ZAR"] == merged["expected_cost"]).sum())

# Recorded cost as a multiple of expected cost
# - 1.0 means the rule holds exactly
merged["ratio"] = merged["Waste_Cost_ZAR"] / merged["expected_cost"]
print(merged["ratio"].describe())

# Do the numbers move together?
# - correlation runs from -1 to 1, and near 0 means no relationship
print("correlation, cost vs quantity:", merged["Waste_Cost_ZAR"].corr(merged["Quantity_Wasted"]))
print("correlation, cost vs expected cost:", merged["Waste_Cost_ZAR"].corr(merged["expected_cost"]))

# A few rows to read
print(merged[["Waste_ID", "Reagent_ID", "Quantity_Wasted", "Cost_Per_Unit_ZAR", "expected_cost", "Waste_Cost_ZAR"]].head(10).to_string())
