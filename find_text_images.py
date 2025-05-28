import fitz  # PyMuPDF
import pandas as pd
import streamlit as st




def text_images(pdf_file):
    # Reads the content into memory as bytes.
    pdf_bytes = pdf_file.read()
    # Loads the PDF into a PyMuPDF Document object from memory rather than from disk
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    results = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        images = page.get_images(full=True)

        results.append({
            "Page": page_num,
            "Text Layer": "Yes" if text.strip() else "No",
            "Image Count": len(images),
        })

        print(f"--- Page {page_num} ---")
        print(f"Text layer present: {'✅ Yes' if text.strip() else '❌ No'}")
        print(f"Number of images: {len(images)}")

        df = pd.DataFrame(results)
        st.dataframe(df)

        # List images
        for i, img in enumerate(images):
            xref = img[0]
            print(f"  Image {i+1} (XREF {xref}) - size: {img[2]}x{img[3]}")
