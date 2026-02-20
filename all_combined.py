import pandas as pd

base_path = "Result csv files/"

projects = pd.read_csv(base_path + "combined_cleaned_data.csv")
env = pd.read_csv(base_path + "Environment.csv")
housing = pd.read_csv(base_path + "Housing_Cleaned.csv")
infra = pd.read_csv(base_path + "Infrastructure_Transportation_Cleaned.csv")
urban = pd.read_csv(base_path + "Urban_Growth_Cleaned.csv")

merged = projects.merge(env, on="District_ID", how="left")
merged = merged.merge(housing, on="District_ID", how="left")
merged = merged.merge(infra, on="District_ID", how="left")
merged = merged.merge(urban, on="District_ID", how="left")

merged.to_csv("Result csv files/final_unified_dataset.csv", index=False)