import streamlit as st
import pdfplumber
import pandas as pd
import io

st.title("PDF Data Extraction and Analysis App")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    st.success(f"Uploaded file: {uploaded_file.name}")
    
     # Convert uploaded file to BytesIO object
    pdf_file = io.BytesIO(uploaded_file.read())

    # Open with pdfplumber
    with pdfplumber.open(pdf_file) as pdf:
        st.info(f"The PDF has {len(pdf.pages)} page(s).")
        
        # Take the first page
        page = pdf.pages[0]

        # Extract table
        table = page.extract_table()

        if table:
            # Convert to pandas DataFrame
            df = pd.DataFrame(table[1:], columns=table[0])
            print(df)

            st.subheader("Extracted Table:")
            st.dataframe(df)

        else:
            st.warning("No table found on the first page.")
