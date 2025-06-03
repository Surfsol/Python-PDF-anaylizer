import fitz  # PyMuPDF
import pandas as pd
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
folder = os.getenv("DOWNLOAD_FOLDER")

malicious_keywords = ["/Acroform", "/JavaScript", "/Launch", "/AA", "/OpenAction", "/SubmitForm", "/XFA"]
def text_images(pdf_file):
    # Reads the content into memory as bytes.
    pdf_bytes = pdf_file.read()
    # Loads the PDF into a PyMuPDF Document object from memory rather than from disk
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    results = []
    for page_num, page in enumerate(doc, start=1):
        # for each page, get text and images
        text = page.get_text()
        images = page.get_images(full=True) # full=True return detailed info for each image.
        flags = []
        images_list = []
        full_page = ''
        chain = ''

        # Extract first 3 characters, check if they are digits
        if len(text) >= 3 and text[:3].isdigit():
            chain = text[:3]

        for kw in malicious_keywords:
            if kw in text:
                flags.append(kw)

        # For each image, get image info
        for i, img in enumerate(images):
            xref = img[0] # get unique image number
            image_info = doc.extract_image(xref) #get image bytes and metadata
            image_bytes = image_info["image"]
            image_ext = image_info["ext"]
            images_list.append(image_ext)
            if image_ext == 'jpx':
                full_page = 'Full'
            if image_ext == 'jpeg' or 'png':
                image_height = image_info["height"]
                image_width = image_info["width"]
                if image_height > 1500 and image_width > 1200:
                    full_page = 'Full'

            
            # Save images to a folder
            # Comment out when you do not want to write the images to a file
            output_dir = folder
            os.makedirs(output_dir, exist_ok=True)
            filename = f"page{page_num}_image{i + 1}.{image_ext}"
            filepath = os.path.join(output_dir, filename)
            # with open(filepath, "wb") as f:
            #     f.write(image_bytes)

            #print(f"Saved image: {filepath}")

        results.append({
            "Page": page_num,
            "Images": len(images),
            "Formats": ", ".join(images_list) if images_list else "",
            "Full Pg Img": full_page,
            "Chain": chain,
            "Text": text,
            "Flags": ", ".join(flags) if flags else ""
        })

    df = pd.DataFrame(results)
    st.dataframe(df)
