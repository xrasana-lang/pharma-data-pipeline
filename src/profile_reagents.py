import pandas as pd

df = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Reagents")
df.info()
print(df.isna().sum())
print(df["Category"].value_counts())

