import pdfplumber
import logging

#set up logging
logging.basicConfig(
    filename="Housing_Zoning.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    #holds all the text
    full_text = ""
    
    with pdfplumber.open("Housing_Zoning_Update_Q1_2024.pdf") as pdf:
        #loop through each page and extract text
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            full_text += text + "\n"
            logging.info(f"Extracted tex from page {i+1}")

#print error message if extraction went wrong
except Exception as e:
    logging.error(f"Error during PDF extraction: {e}")

#open new file for writing and add extracted text 
with open("Housing_Zoning_Extracted.txt", "w", encoding="utf-8") as f:
    f.write(full_text)