import pandas as pd
import re
import logging
import pprint
import numpy as np
import data_cleaning

# Setup Logging
logging.basicConfig(filename='./LOGS/Housing_Transformation.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_housing_data(file_name, units_pattern):
    #We used this function, but at the end, we decided to not.
    all_data = []
    
    logging.info(f"Processing file: {file_name}")
    if "2023" in file_name:
        file_period = "2023"
    elif "2024" in file_name:
        file_period = "2024_Q1"
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # IMPROVED SPLITTING LOGIc
        # This regex matches BOTH "District: D01" (Housing PDF) and "District D01" (Urban PDF)
        # The '?' after the colon makes it optional.
        parts = re.split(r'(District[:\s]*D\d+[^\n\r]*)', content, flags=re.IGNORECASE)
        
        # Loop through parts (Header + Body)
        for i in range(1, len(parts), 2):
            header = parts[i]
            body = parts[i+1] if i+1 < len(parts) else ""
            
            row = {}
            # Add year to the row dictionary
            row['Report_period'] = file_period
            #HEADER EXTRACTION
            # Extract ID (D01)
            d_id = re.search(r'(D\d+)', header)
            if d_id:
                row['District_ID'] = d_id.group(1)
            # BODY EXTRACTION 
            
            # UNITS: Catches "Units:", "New Units:", "Units Authorized:", "Approved Units:", "Total... units:"
            # The '.*?' allows for text between the word "Units" and the number (like "Units approved in 2023:") 
            units = re.search(units_pattern, body, re.IGNORECASE)
            #pprint.pprint(units)
            if units:
                row['New_Residential_Units'] = units.group(1)
                row['Old_Residential_Units'] = units.group(2)
                row['YoY_Change_%'] = units.group(3)
            # Add to list if valid
            if 'District_ID' in row:
                all_data.append(row)
            
    except FileNotFoundError:
        logging.error(f"File not found: {file_name}")
    
    return all_data


def parse_data(file_name):
    all_data = {}


    logging.info(f"Processing file: {file_name}")
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read()

        section_pattern = (
                r'(?:District Infrastructure Metrics'
                r'|New Residential Units and Green Space \(2023 vs 2022\)'
                r'|New Units by District \(Q1 2024 vs Q1 2023\))'  
                r'(.*?)'                                         
                r'(?=Figure 1:|Notes:|NOTES?:|PERMIT #|$)')
        
        search_table = re.search(
            section_pattern, 
            content,
            flags = re.DOTALL)
        
        table = search_table.group().split('\n')
        table_clean = [x for x in table if x and x.strip()]

        col_names = table_clean[1].split(" ")
        seen = {}
        for col in col_names:
            if col not in all_data:
                seen[col] = 0
                all_data[col] = []
            else:
                seen[col] += 1
                all_data[f"{col}_{seen[col]}"] = []
    
        for i in range(2,len(table_clean)):
            row= table_clean[i].split(" ")

            for i, key in enumerate(all_data):
                all_data[key].append(row[i])


    except FileNotFoundError:
        logging.error(f"File not found: {file_name}")

    return all_data


#  EXECUTION
def main():

    files_to_process = [
        "Housing_Zoning_Update_Q1_2024_extracted.txt",
        "Infrastructure_Transportation_Summary_2024_extracted.txt",
        "Urban_Growth_Report_2023_extracted.txt"
        ]

    #Getting all the datas from each txt file, then turn it to df
    logging.info("Starting Transformation Phase...")

    df_list = []
    for file in files_to_process:
        data = parse_data(file)
        df = pd.DataFrame(data)
        df_clean = data_cleaning.data_cleaner(df)
        df_list.append(df_clean)

    #Only get necessary col from df
    df_housing = df_list[0]
    df_housing_final = df_housing[['District_ID','Zoning_Type','Units_Q1_2024','Units_Q1_2023','YoY_Change_%']]

    df_infra = df_list[1]
    df_infra_final = df_infra[['District_ID','Road_2024_km','Road_2023_km','YoY_%']]

    df_urban_final = df_list[2]
  

    #to csv
    df_housing_final.to_csv('./Result csv files/Housing_Cleaned.csv', index=False)
    df_infra_final.to_csv('./Result csv files/Infrastructure_Transportation_Cleaned.csv', index=False)
    df_urban_final.to_csv('./Result csv files/Urban_Growth_Cleaned.csv', index=False)


main()

"""
Documentation/Reflection (For transform_house.py)

-I ran into an issue where the code missed some districts because the PDFs were inconsistent. 
Some said "District: D01" with a colon, and others just said "District D01". I had to update 
my regex pattern to handle both versions so I didn't lose any data.

-I also had trouble extracting the "New Residential Units" because the reports used 
different labels like "Units Approved" or "Total Units". I researched regex techniques and 
built a flexible pattern using "OR" logic to catch all those variations at once.

- I attempted to extract 'Zoning Type' to provide more detail, but the data was 
not consistent across the different PDF reports. For example, while the first 
report had clear zoning categories, the others either left the field out or 
used that section for different information. To ensure the final CSV remained clean 
and accurate, I decided to remove this column rather than include 
misleading or missing information.

-I used the logging library instead of print statements because it helps keep track of 
errors better. I watched some tutorials to understand how to set it up properly.


(For transform_house_fixed.py)

-After discussing as a group, we concluded that extracting the necessary information 
from the current state of the code would be difficult. Therefore, we decided to create 
a new function and build a table that conforms to the schema.

-The previous function design had difficulty to extract the necessary information from 
each of the three PDFs, but the new function design has made this possible.

-The new function identified the location of each table within the respective PDFs and 
extracted all information from them. It then converted this data into a pandas DataFrame 
and cleaned it.

-We initially converted the PDF to a TXT file, but that actually increased the difficulty. 
If we had designed it to extract the PDF tables from the start, we might have been able 
to extract the data much more easily.
"""