"""
Description:
This code merges project-level and district-level datasets into a single
unified dataset. The final dataset preserves one row per project (Project_ID)
and appends district-level contextual features.

Primary Key: project_id
Foreign Key: district_id
"""

import pandas as pd


#1. Load cleaned datasets


base_path = "Result csv files/"

projects = pd.read_csv(base_path + "combined_cleaned_data.csv")
environment = pd.read_csv(base_path + "Environment.csv")
housing = pd.read_csv(base_path + "Housing_Cleaned.csv")
infrastructure = pd.read_csv(base_path + "Infrastructure_Transportation_Cleaned.csv")
urban_growth = pd.read_csv(base_path + "Urban_Growth_Cleaned.csv")


#2. Validate key integrity before merge


# Ensure district-level tables contain unique district_id values
assert environment["District_ID"].duplicated().sum() == 0, "Duplicate District_ID in Environment"
assert housing["District_ID"].duplicated().sum() == 0, "Duplicate District_ID in Housing"
assert infrastructure["District_ID"].duplicated().sum() == 0, "Duplicate District_ID in Infrastructure"
assert urban_growth["District_ID"].duplicated().sum() == 0, "Duplicate District_ID in Urban Growth"


#3. Merge Datasets


# Start with project-level dataset
merged = projects.merge(environment, on="District_ID", how="left")
merged = merged.merge(housing, on="District_ID", how="left")
merged = merged.merge(infrastructure, on="District_ID", how="left")
merged = merged.merge(urban_growth, on="District_ID", how="left")

# 4. Post-Merge Validation


# Ensure primary key uniqueness is preserved
assert merged["Project_ID"].duplicated().sum() == 0, "Primary key violation: project_id not unique"

# Check for missing values introduced by joins
null_summary = merged.isnull().sum()


# 5. Export Final Dataset


output_path = base_path + "final_unified_dataset.csv"
merged.to_csv(output_path, index=False)

print("Final dataset successfully created.")
print("Total rows:", len(merged))
print("Unique projects:", merged["Project_ID"].nunique())