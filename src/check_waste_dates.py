# Waste dates and status against batch records
# - does waste happen after the batch was made?
# - do "Expired" waste records fall after the batch expiry date?
# - read only, changes nothing
import pandas as pd

# File path
FILE = "data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx"

# Load both tables
waste = pd.read_excel(FILE, sheet_name="Waste_Transactions")
batches = pd.read_excel(FILE, sheet_name="Batch_Inventory")

# Attach batch dates and status to each waste record
joined = waste.merge(
    batches[["Batch_ID", "Manufacture_Date", "Expiry_Date", "Current_Status"]],
    on="Batch_ID",
    how="left",
)
print("rows:", len(waste), "after join:", len(joined))

# Waste before the batch was made?
# - days from manufacture to waste, negative = impossible
days_since_made = (joined["Date"] - joined["Manufacture_Date"]).dt.days
print("waste before manufacture:", (days_since_made < 0).sum())

# Waste against the expiry date
# - days from expiry to waste, negative = wasted before it expired
days_after_expiry = (joined["Date"] - joined["Expiry_Date"]).dt.days

# Records with reason Expired
expired = joined["Waste_Reason"] == "Expired"
print("Expired records:", expired.sum())
print("Expired records dated before expiry:", (days_after_expiry[expired] < 0).sum())
print(days_after_expiry[expired].describe())

# Batch status on waste records
# - all waste records, then only the Expired ones
print(joined["Current_Status"].value_counts())
print(joined.loc[expired, "Current_Status"].value_counts())
