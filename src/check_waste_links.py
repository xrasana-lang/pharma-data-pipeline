# Waste_Transactions link checks
# - do waste records point at real batches and reagents?
# - does the waste reagent match the batch reagent?
# - read only, changes nothing
import pandas as pd

# File path
FILE = "data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx"

# Load the three tables
waste = pd.read_excel(FILE, sheet_name="Waste_Transactions")
batches = pd.read_excel(FILE, sheet_name="Batch_Inventory")
reagents = pd.read_excel(FILE, sheet_name="Reagents")

# Orphans
# - waste values with no match in the other table
print("waste -> batches orphans:", (~waste["Batch_ID"].isin(batches["Batch_ID"])).sum())
print("waste -> reagents orphans:", (~waste["Reagent_ID"].isin(reagents["Reagent_ID"])).sum())

# Does the waste reagent match the batch reagent?
# - suffixes tell the two Reagent_ID columns apart after the join
joined = waste.merge(
    batches[["Batch_ID", "Reagent_ID"]],
    on="Batch_ID",
    how="left",
    suffixes=("_waste", "_batch"),
)
print("rows:", len(waste), "after join:", len(joined))
print("waste reagent equals batch reagent:", (joined["Reagent_ID_waste"] == joined["Reagent_ID_batch"]).sum())

# Batches wasted more than once
# - value_counts() counts waste records per batch
per_batch = waste["Batch_ID"].value_counts()
print("batches with waste records:", len(per_batch))
print("batches with more than one waste record:", (per_batch > 1).sum())
