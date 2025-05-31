import subprocess
import streamlit as st
import pandas as pd
import xml.dom.minidom
import subprocess
from malware_detect.pdfid import PDFiD

def extract_pdf_object_with_mal(uploaded_pdf):
    if uploaded_pdf is not None:
        # Save PDF to disk for tools that require file path
        pdf_path = "temp_uploaded.pdf"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.read())
    object_ids = []
  
    try:
        result = subprocess.run(
            ['python', 'malware_detect/pdf-parser.py', pdf_path, '-s', '/Launch'],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        
        for line in output.splitlines():
            if line.startswith('obj '):
                parts = line.split()
                if len(parts) >= 2 and parts[1].isdigit():
                    object_ids.append(parts[1])
    
    except Exception as e:
        return [f"Error running pdf-parser: {e}"]
    return object_ids
        


# --- Helper: Inspect full object contents
def get_pdf_object_details(uploaded_pdf, object_id):
    print('Object ID:', object_id)

    # Save uploaded file to disk
    pdf_path = "temp_uploaded.pdf"
    if uploaded_pdf is not None:
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.read())

    try:
        result = subprocess.run(
            ['python', 'malware_detect/pdf-parser.py', pdf_path, '-s', '/Fields'],
            capture_output=True,
            text=True
        )
        return result.stdout
    except Exception as e:
        return f"Error reading object {object_id}: {e}"
    
def inspect_mal_location(pdf):
    if pdf is not None:
        # Save uploaded PDF to disk
        with open("temp_uploaded.pdf", "wb") as out_file:
            out_file.write(pdf.read())

        # Now read it back as binary
        with open("temp_uploaded.pdf", "rb") as f:
            content = f.read()

        # Search for the object by ID
        location = content.find(b"652 0 obj")
        if location != -1:
            print(f"Object 652 found at byte offset: {location}")
            return location
        else:
            print("Object 652 not found.")
            return None





def detect_malware(uploaded_pdf_malware):
    if uploaded_pdf_malware is not None:
        # Save PDF to disk for tools that require file path
        pdf_path = "temp_uploaded.pdf"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf_malware.read())

        # Run PDFiD to detect suspicious keywords
        xml_dom = PDFiD(pdf_path)
        keywords = xml_dom.getElementsByTagName("Keyword")
        data = []
        for keyword in keywords:
            name = keyword.getAttribute("Name")
            count = int(keyword.getAttribute("Count"))
            if count > 0:
                data.append((name, count))

        if data:
            df = pd.DataFrame(data, columns=["Keyword", "Count"])
            st.subheader("Suspicious PDF Features Detected")
            st.dataframe(df)

            # Detect and flag /AA and /AcroForm
            flagged = []
            flag_list = []
            for keyword, count in data:
                if keyword in ["/AA", "/AcroForm"]:
                    flagged.append(f"{keyword} (count: {count})")
                    flag_list.append(keyword)
            if flagged:
                st.warning(f"⚠️ Detected potentially risky features: {', '.join(flagged)}")

                st.info("Inspecting `/AA` object contents for potential auto-actions...")
        else:
            st.success("✅ No suspicious keywords found in the PDF.")

