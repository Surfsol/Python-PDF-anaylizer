import pdfplumber
import io
import re

def parse_pdf_to_table(uploaded_file):
    if uploaded_file is None:
        return []
    
     # Convert uploaded file to bytes in memory
    pdf_bytes = uploaded_file.read()
    # 🔍 Diagnostic printouts
    print("pdf_bytes type:", type(pdf_bytes))
    print("pdf_bytes length:", len(pdf_bytes))
    print("First 20 bytes:", pdf_bytes[:20])
    
    pdf_file = io.BytesIO(pdf_bytes)

    
    
    all_rows = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            raw_text = page.extract_text()

            if not raw_text:
                continue

            lines = raw_text.split('\n')

            for line in lines:
                columns = re.split(r'\s{2,}', line.strip())
                if len(columns) >= 2:
                    all_rows.append(columns)

    return all_rows
