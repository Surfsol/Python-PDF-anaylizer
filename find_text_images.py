import fitz  # PyMuPDF
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
folder = os.getenv("DOWNLOAD_FOLDER")


def text_images(pdf_file):
    # Reads the content into memory as bytes.
    pdf_bytes = pdf_file.read()
    # Loads the PDF into a PyMuPDF Document object from memory rather than from disk
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    results = []
    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        images = page.get_images(full=True) # full=True return detailed info for each image.
        jpx = ''

       
        output_dir = folder
        os.makedirs(output_dir, exist_ok=True)

        # chain emails 1, 16, 19, 21, 32, 43, 46, 47,, 49, 59, 71, 74, 78
        #.jpx pages include:  4, 5, 6, 7, 10, 11, 14, 15, 31, 35, 42, 44, 51, 53 57, 58, 64, 67

        #List images
        for i, img in enumerate(images):
            xref = img[0] # get unique image number
        
            image_info = doc.extract_image(xref) #get image bytes and metadata
            image_bytes = image_info["image"]
            image_ext = image_info["ext"]
            print('image', image_ext)
            if image_ext == 'jpx':
                jpx = 'T'



            filename = f"page{page_num}_image{i + 1}.{image_ext}"
            filepath = os.path.join(output_dir, filename)
            
            # Comment out when you do not want to write the images to a file
            with open(filepath, "wb") as f:
                f.write(image_bytes)

            #print(f"Saved image: {filepath}")

        results.append({
            "Page": page_num,
            "Image Count": len(images),
            "JPX": jpx,
            "Text": text
        })

    df = pd.DataFrame(results)
    st.dataframe(df)
