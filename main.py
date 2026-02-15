import pandas as pd
import logging

# Setup Logging
logging.basicConfig(
    filename="data_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    logging.info("Starting CSV extraction process.")

    # Extract
    projects = pd.read_csv("City_Development_Projects.csv")
    districts = pd.read_csv("Population_Economic_Indicators.csv")

    logging.info("CSV files successfully loaded.")

    # Clean Projects Data

    # Remove duplicate rows

    projects = projects.drop_duplicates()

    # Standardize Project_Status
    projects["Project_Status"] = projects["Project_Status"].str.lower().str.strip()

    # Handle missing Estimated_Units
    projects["Estimated_Units"] = pd.to_numeric(
        projects["Estimated_Units"], errors="coerce"
    )

    # Standardize dates
    projects["Project_Start_Date"] = pd.to_datetime(
        projects["Project_Start_Date"], errors="coerce"
    )

    logging.info("Projects data cleaned.")

    # Clean District Data

    # Remove duplicate District_ID rows (keep first)
    districts = districts.drop_duplicates(subset=["District_ID"], keep="first")

    # Standardize district names
    districts["District_Name"] = districts["District_Name"].str.title().str.strip()

    # Clean Median_Income
    districts["Median_Income"] = (
        districts["Median_Income"]
        .replace(",", "", regex=True)
    )
    districts["Median_Income"] = pd.to_numeric(
        districts["Median_Income"], errors="coerce"
    )

    # Clean Employment_Rate
    districts["Employment_Rate"] = (
        districts["Employment_Rate"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )
    districts["Employment_Rate"] = pd.to_numeric(
        districts["Employment_Rate"], errors="coerce"
    )

    # Convert percentages properly
    districts["Employment_Rate"] = districts["Employment_Rate"].apply(
        lambda x: x/100 if x and x > 1 else x
    )

    logging.info("District data cleaned.")

    # Merge tables
    combined = pd.merge(projects,districts,on="District_ID",how="left")

    logging.info("Merge completed successfully.")

    combined.to_csv("combined_cleaned_data.csv", index=False)

    logging.info("Pipeline completed and file saved.")

except Exception as e:
    logging.error(f"An error occurred: {e}")