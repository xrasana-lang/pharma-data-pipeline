import pandas as pd
df = pd.read_excel("data/raw/Ubuntu_Pharma_Inventory_Dataset.xlsx", sheet_name="Suppliers")
print(df.shape)
print(df.columns)
print(df["Supplier_Name"].value_counts())
merck = df[df["Supplier_Name"].str.contains("merck", case=False)]
print(merck[["Supplier_ID", "Supplier_Name", "Country"]])