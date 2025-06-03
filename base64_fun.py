import base64
import streamlit as st
import datetime

def base64_decoder(uploaded_base64_file):
    # Read and decode base64 data
    raw_text = uploaded_base64_file.read().decode("utf-8")  # decode bytes to string
    # remove new lines and whitespaces for decoding
    base64_data = "".join(raw_text.strip().splitlines())

    try:
        # Get current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")
        # Create filename with timestamp
        filename = f"decoded_foia_{timestamp}.pdf"
        # First decode and write the PDF to disk
        with open(filename, "wb") as outfile:  # b = binary, pdf files are binary
            outfile.write(base64.b64decode(base64_data))

        # Then reopen it in binary mode for the download button
        with open(filename, "rb") as f:  # b = binary, pdf files are binary
            st.download_button(
                label="Download decoded PDF",
                data=f,
                file_name= filename,
                mime="application/pdf"
            )
        st.success(f"PDF successfully decoded and saved as 'decoded_foia_{timestamp}.pdf'")
    except Exception as e:
        st.error(f"Failed to decode PDF: {e}")