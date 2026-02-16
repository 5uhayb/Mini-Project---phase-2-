import pandas as pd
import re
import logging

# Setup Logging
logging.basicConfig(filename='./LOGS/Housing_Transformation.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_housing_data(file_list):
    all_data = []
    
    for file_name in file_list:
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
                
                # Extract Name (Downtown)
                d_name = re.search(r'-\s*([A-Za-z\s]+)', header)
                if d_name:
                    row['District_Name'] = d_name.group(1).strip()
                
                # BODY EXTRACTION 
                
                # UNITS: Catches "Units:", "New Units:", "Units Authorized:", "Approved Units:", "Total... units:"
                # The '.*?' allows for text between the word "Units" and the number (like "Units approved in 2023:")
                
                units_pattern = r'(?:Units|New Units|Authorized|Approved|Total new residential units|Units_Q1_2023).*?:\s*(\d+)'                
                units = re.search(units_pattern, body, re.IGNORECASE)
                
                if units:
                    row['New_Residential_Units'] = int(units.group(1))

                # Add to list if valid
                if 'District_ID' in row:
                    all_data.append(row)
                    
        except FileNotFoundError:
            logging.error(f"File not found: {file_name}")
    
    return all_data

#  EXECUTION 
files_to_process = [
    "Housing_Zoning_Update_Q1_2024_extracted.txt",
    "Infrastructure_Transportation_Summary_2024_extracted.txt",
    "Urban_Growth_Report_2023_extracted.txt"
]

logging.info("Starting Transformation Phase...")
data = parse_housing_data(files_to_process)

df = pd.DataFrame(data)
    
    # Clean up duplicates
df = df.drop_duplicates(subset=['District_ID', 'New_Residential_Units'])
    
    # Sort for cleanliness
df = df.sort_values('District_ID')
    
    # Select ONLY the clean columns. This removes 'Zoning_Type' automatically.
df = df[['District_ID', 'District_Name', 'Report_period', 'New_Residential_Units']]    
    # Save to CSV
df = df.reset_index(drop=True)
df.to_csv('Housing_Zoning_Cleaned.csv', index=False)
print("Success, Created 'Housing_Zoning_Cleaned.csv' with", len(df), "rows.")
print(df)


"""
Documentation/Reflection

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
- Another significant challenge was managing the inconsistency between the Full Year 2023 report and the 
Q1 2024 update, which I resolved by standardizing the 'Report_Period' column to ensure an accurate 
'apples-to-apples'comparison.
-I used the logging library instead of print statements because it helps keep track of 
errors better. I watched some tutorials to understand how to set it up properly.

"""