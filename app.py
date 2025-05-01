import streamlit as st
import pdfplumber
import pandas as pd
import io
import re
#from pdf_parser import parse_pdf_to_table

st.title("PDF Data Extraction and Analysis App")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.success(f"Uploaded file: {uploaded_file.name}")
    
     # Convert uploaded file to bytes in memory
    pdf_bytes = uploaded_file.read()
    # 🔍 Diagnostic printouts

    
    pdf_file = io.BytesIO(pdf_bytes)

    all_rows = []
    

    # Open with pdfplumber
    with pdfplumber.open(pdf_file) as pdf:
        st.info(f"The PDF has {len(pdf.pages)} page(s).")
        
        # Take the first page
        page = pdf.pages[0]

        st.subheader("Raw Text Extracted from PDF:")

        # Extract word object from the page
        word_obj_list = page.extract_words()
        print(word_obj_list[0])

        #list to capture coordinates
        coordinate_dict = {
            'foia': [],
            'open': [],
            'close': []
            }
        #find coordinates 
        for obj in word_obj_list:
             # if the string in obj['text'] begins with 'F-'
             if obj['text'][0] == 'F' and obj['text'][1] == '-':
             #save text and coordinate into a list
                if obj['x0'] not in coordinate_dict['foia']:
                    coordinate_dict['foia'].append(obj['x0'])
        print(coordinate_dict)

    #     #replace whitespace with underline
    #     text_under = raw_text.replace(' ', '_')
    #     st.text(text_under)
    #     #split at end of line
    #     lines = raw_text.split('\n')
        
    #     for line in lines:
    #             st.text(line)
    #             #if line starts with F- put into a list with 12 items, starting at 0
    #             #in most cases will be 7 items the other 5 will be added later
    #             foia_list =  [None] * 12
    #             if line[0] == 'F' and line[1] == '-':
    #                  f_num_start = line.split()[0]
    #                 # print('f_num',f_num_start)
    #                  st.text(type(line))

    #             #if the row ends in date format, check to see if a date preceeds that date

    #             #ch

    #             columns = re.split(r'\s{2,}', line.strip())
                
    #             if len(columns) >= 1:
    #                 all_rows.append(columns)

    # if all_rows:
    #     # Try to create a DataFrame
    #     try:
    #         df = pd.DataFrame(all_rows)

    #         st.subheader("Extracted Table from PDF (Text Split by Spaces):")
    #         st.dataframe(df)
    #     except Exception as e:
    #         st.error(f"Failed to create table: {e}")
    # else:
    #     st.warning("No table found on the first page.")
