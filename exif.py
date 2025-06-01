import os
import subprocess
import streamlit as st
from dotenv import load_dotenv

def run_exiftool_on_folder():
    st.title("EXIF Metadata Viewer for Extracted Images")
    folder_path = os.getenv("DOWNLOAD_FOLDER")
    exiftool_path = os.getenv("EXIFTOOL")

    image_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(('.jpg', '.jpeg', '.jpx', '.png'))
    ]

    if not image_files:
        st.warning("No image files found in the folder.")
        return

    for filename in sorted(image_files):
        file_path = os.path.join(folder_path, filename)
        st.subheader(f"📁 Metadata for: {filename}")

        try:
            result = subprocess.run(
                [exiftool_path, file_path],
                capture_output=True,
                text=True
            )
            st.code(result.stdout, language='text')
        except Exception as e:
            st.error(f"Failed to process {filename}: {e}")

# Example usage:
# folder = "C:/Users/surf/Documents/foia/DOS/extracted_images/foia_2024"
# run_exiftool_on_folder(folder)
