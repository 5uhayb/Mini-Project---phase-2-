import pdfplumber
import logging

#set up logging
logging.basicConfig(
    filename="./LOGS/pdf_extraction.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#make list of the three pdfs
pdf_files = [
    "Housing_Zoning_Update_Q1_2024.pdf",
    "Infrastructure_Transportation_Summary_2024.pdf",
    "Urban_Growth_Report_2023.pdf"
]

#loop through pdfs
for file in pdf_files:
    #empty string to store all the pdf text
    full_text = ""
    
    try:
        with pdfplumber.open(file) as pdf:
            #loop through each page and extract text
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    full_text += text + "\n\n\n"
                    logging.info(f"Extracted tex from page {i+1}")
                else:
                    logging.warning(f"{file} - No text on page {i+1}")

        #save each extracted file separately
        output_name = file.replace(".pdf", "_extracted.txt") 
        with open(output_name, "w", encoding="utf-8") as f:
            f.write(full_text)

        logging.info(f"{file} - Extraction completed")

    except Exception as e:
        logging.error(f"{file} - Error: {e}")
    



"""

Documentation


-Accessed and read the pdfs with no problem.

-I never had experience with logging so I had to watch a few youtube 
videos to see how it worked and was able to set it up pretty quick.

-Then I made a for loop to go through the list of the three pdfs
and extract all the text from each one and add that text to the
full_text empty string.

-At first when I ran my code, all the text from each page just merged 
into one big paragraph which I then had to separate them by using \n
to indicate when a new page began.

-After that I made sure to save each of the extracted pdfs to its own 
new file.

"""