import subprocess
import streamlit as st
import pandas as pd
import xml.dom.minidom
import subprocess
from malware_detect.pdfid import PDFiD

def extract_pdf_object_with_mal(pdf_path, flagged):
    object_ids = []
    for id in flagged:
        try:
            print('34r345', id)
            result = subprocess.run(
                ['python', 'malware_detect/pdf-parser.py', pdf_path, '-s', '/AA'],
                capture_output=True,
                text=True
            )
            print('899RESULLLLLLTTTTS'.result)
            output = result.stdout.strip()
            
            for line in output.splitlines():
                if line.startswith('obj '):
                    parts = line.split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        object_ids.append(parts[1])
        
        except Exception as e:
            return [f"Error running pdf-parser: {e}"]
    print('Idssssssssss', object_ids)
    return object_ids
        


# --- Helper: Inspect full object contents
def get_pdf_object_details(pdf_path, object_id):
    print('objectttt list line 36', object_id)
    try:
        result = subprocess.run(
            ['python', 'malware_detect/pdf-parser.py', pdf_path, '-o', object_id, '-d'],
            capture_output=True,
            text=True
        )
        print('9999999999', result)
        return result.stdout
    except Exception as e:
        return f"Error reading object {object_id}: {e}"


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

