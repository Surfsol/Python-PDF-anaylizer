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
    print("pdf_bytes type:", type(pdf_bytes))
    print("pdf_bytes length:", len(pdf_bytes))
    print("First 20 bytes:", pdf_bytes[:20])
    
    pdf_file = io.BytesIO(pdf_bytes)

    all_rows = []
    

    # Open with pdfplumber
    with pdfplumber.open(pdf_file) as pdf:
        st.info(f"The PDF has {len(pdf.pages)} page(s).")
        
        # Take the first page
        page = pdf.pages[0]

        # Extract raw text from the page
        raw_text = page.extract_text()
        st.subheader("Raw Text Extracted from PDF:")
        #st.text(raw_text)
        
        lines = raw_text.split('\n')
        print('FFFFFFFFF',len(lines))
        
        for line in lines:
                columns = re.split(r'\s{2,}', line.strip())
                print('the column',len(columns), columns)
                if len(columns) >= 1:
                    print('in colummns')
                    all_rows.append(columns)
                    
                    

        
       



    if all_rows:
        # Try to create a DataFrame
        try:
            df = pd.DataFrame(all_rows)

            st.subheader("Extracted Table from PDF (Text Split by Spaces):")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Failed to create table: {e}")
    else:
        st.warning("No table found on the first page.")
