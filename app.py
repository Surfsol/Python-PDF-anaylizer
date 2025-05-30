import streamlit as st
import pdfplumber
import pandas as pd
import io
import re
from datetime import datetime
from coordinates import coord_page
from db import save_to_sqlite
from db import fetch_all_data
import base64

#from pdf_parser import parse_pdf_to_table


st.write("Max upload size (MB):", st.get_option("server.maxUploadSize"))

st.title("PDF Data Extraction and Analysis App")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])





st.title("Base64 to PDF Decoder")

# Show current upload size limit
st.write("Max upload size (MB):", st.get_option("server.maxUploadSize"))

# File uploader
uploaded_base64_file = st.file_uploader("Upload base64 file (.txt)", type=["txt"])

if uploaded_base64_file is not None:
    # Read and decode base64 data
    raw_text = uploaded_base64_file.read().decode("utf-8")  # decode bytes to string
    base64_data = "".join(raw_text.strip().splitlines())

    # Fix base64 padding
    missing_padding = len(base64_data) % 4
    if missing_padding:
        base64_data += '=' * (4 - missing_padding)

    try:
        # First decode and write the PDF to disk
        with open("decoded_foia.pdf", "wb") as outfile:
            outfile.write(base64.b64decode(base64_data))

        # Then reopen it in binary mode for the download button
        with open("decoded_foia.pdf", "rb") as f:
            st.download_button(
                label="Download decoded PDF",
                data=f,
                file_name="decoded_foia_64.pdf",
                mime="application/pdf"
            )

        st.success("PDF successfully decoded and saved as 'decoded_foia.pdf'")
    except Exception as e:
        st.error(f"Failed to decode PDF: {e}")

    





#list to capture foia
foia_list = []

foia_late = []

if uploaded_file is not None:
    st.success(f"Uploaded file: {uploaded_file.name}")
    
     # Convert uploaded file to bytes in memory
    pdf_bytes = uploaded_file.read()
    # 🔍 Diagnostic printouts

    
    pdf_file = io.BytesIO(pdf_bytes)
    st.write("Uploaded file size:", len(pdf_file.getvalue()))


    all_rows = []
    
    print('NEWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW')

    # Open with pdfplumber
    with pdfplumber.open(pdf_file) as pdf:
        st.info(f"The PDF has {len(pdf.pages)} page(s).")
        
        # Take the first page
        page = pdf.pages[0]

        st.subheader("Raw Text Extracted from PDF:")

        # Extract word object from the page
        word_obj_list = page.extract_words()

        
       # 33333 Each page need to run 

        coordinate_dict = coord_page( word_obj_list, page)

        print('COORDINATE DICTIONARY',coordinate_dict)
        st.write('Coordinates')
        st.write(coordinate_dict)
        # coordinate_dict= {'foia': 19.84, 'open': 685.4, 'close': 718.579757588}

        # Search dates, find out of range
        date_obj = {'foia':"", 'name': "", 'open': None, 'close': None, 'report': '10/01/2024', 'page': page.page_number, 'top': 0, 'bottom': 0}

        date_list = []

        for page in pdf.pages:


            date_obj_list = page.extract_words()

            for idx, obj in enumerate(date_obj_list):

                if obj['x0'] >= (coordinate_dict['open'] - 1) and obj['x0'] < coordinate_dict['close']:
                    
                    try:
                        match = re.search(r"\b\d{1,2}/\d{1,2}/\d{4}", obj['text']) # match open date
                        if (date_obj_list[idx + 1]['x0'] > coordinate_dict['close']) and (round(date_obj_list[idx + 1]['top']) == round(obj['top'])): # if close date exist, match it
                            match_close = re.search(r"\b\d{1,2}/\d{1,2}/\d{4}", date_obj_list[idx + 1]['text']) 

                        # check match and range, check for close date
                        # if get to date and FOIA is missing, make FOIA Missing and attach
                        
                        if match:
                            date_obj['open'] = match.group()
                            date_obj['top'] = obj['top']
                            date_obj['page'] = page.page_number
        
                            if match_close:
                                date_obj['close'] = match_close.group()
                                if date_obj['close'] < date_obj['report']:
                                    date_obj['bottom'] = obj['bottom']
                                    foia_late.append(date_obj.copy())
                                    match_close = None
                            # push 
                            date_list.append(date_obj.copy())
                            #reset date_obj
                            date_obj = {'foia':"", 'name': "", 'open': None, 'close': None, 'report': '10/01/2024', 'page': page.page_number, 'top': 0, 'bottom': 0} 
                    except:
                        pass
                continue

        df_date_late = pd.DataFrame(foia_late)
        st.dataframe(df_date_late)
        # df_date = pd.DataFrame(date_list)
        # st.dataframe(df_date)

        # Add FOIA number and name to out of range dates.

        #foia_late
        for item in foia_late:
            page = pdf.pages[item['page'] - 1]

            word_obj_list = page.extract_words()

            coordinate_page = coord_page(word_obj_list, page)

            item['foia'] = 'Missing'
            for obj in word_obj_list:
                # search within x and y range
                if obj['x0'] < coordinate_page['name'] and obj['top'] > (item['top'] - 7) and obj['bottom'] < (item['top'] + 14):
                    if item['foia'] == 'Missing':
                        item['foia'] = obj['text']
                    else:
                        item['foia'] = item['foia'] + obj['text']

                # check bottom range
                if obj['bottom'] < (item['top'] + 13) and obj['top'] > (item['top'] - 7) and obj['x0'] > coordinate_page['name'] and obj['x0'] < coordinate_page['name_end']:
                    if item['name'] == '':
                        item['name'] = obj['text']
                    else:
                        item['name'] = item['name'] + " " + obj['text']
                    

        st.write('Updated Out of Range')
        df_date_late = pd.DataFrame(foia_late)
        st.dataframe(df_date_late)

       
        
        if foia_late:
            result = save_to_sqlite(foia_late)
            print('result', result)
            if result > 0:
                st.write(f"✅ {result} record(s) uploaded successfully!")
            else:
                st.write(f"❌ Upload failed: {result}")

        all_data_df = fetch_all_data()
        st.subheader('Data from database')
        st.dataframe(all_data_df)


        for page in pdf.pages:
            text = page.extract_text()

            
            word_obj_list = page.extract_words()
            f_obj = {'foia':"", 'name': "", 'open': None, 'close': None, 'report': '10/01/2024', 'page': page.page_number, 'top': 0}
            f_obj['page'] = page.page_number
            for idx, obj in enumerate(word_obj_list): 
                if abs(obj['x0'] - coordinate_dict['foia']) <= 2:
                    if len(obj['text']) > 4 and not obj['text'][0].isdigit():
                        f_obj['foia'] = obj['text']
                        f_obj['top'] = obj['top']
                    # Last numbers of FOIA
                    elif len(obj['text']) == 5 and obj['text'][0].isdigit() and obj['top'] - f_obj['top'] < coordinate_dict['y-range']: 
                        # complete full FOIA id
                        full_id = f_obj['foia'] + obj['text']
                        f_obj['foia'] = full_id
                        # if already have date open add to foia list
                        if f_obj['open'] != None or f_obj['close'] != None:
                            # ADD END OF NAME, SO DOES NOT RUN OVER
                            
                            foia_list.append(f_obj.copy())
                            if f_obj['close'] != None and f_obj['close'] < f_obj['report']:
                                     foia_late.append(f_obj.copy())
                        #reset f_obj
                        f_obj = {'foia':"", 'name': "", 'open': None, 'close': None, 'report': '10/01/2024', 'page': page.page_number, 'top': 0}
                    continue

                elif obj['x0'] >= (coordinate_dict['name'] - 1) and obj['x0'] < coordinate_dict['name_end']:
                    if f_obj['name'] != "":
                        f_obj['name'] = f_obj['name'] + " " + obj['text']
                    else: 
                        f_obj['name'] = obj['text']

                elif obj['x0'] >= coordinate_dict['open'] - 2 and obj['x0'] < coordinate_dict['close']:
                    try:
                        match = re.search(r"\b\d{1,2}/\d{1,2}/\d{4}\b", obj['text'])
                        if word_obj_list[idx + 1]['x0'] >= coordinate_dict['close']:
                            match_close = re.search(r"\b\d{1,2}/\d{1,2}/\d{4}", word_obj_list[idx + 1]['text'])
                        # check match and range, check for close date
                        # if get to date and FOIA is missing, make FOIA Missing and attach

                        if match and f_obj['foia'] == "":
                             f_obj['open'] = match.group()
                             f_obj['top'] = obj['top']
                             f_obj['foia'] = "Missing"
                             if match_close and round(word_obj_list[idx + 1]['top']) == round(obj['top']) :
                                 f_obj['close'] = match_close.group()
                                 if f_obj['close'] < f_obj['report']:
                                     foia_late.append(f_obj.copy())
                             # push 
                             foia_list.append(f_obj.copy())
                            #reset f_obj
                             f_obj = {'foia':"", 'name': "", 'open': None, 'close': None, 'report': '10/01/2024', 'page': page.page_number, 'top': 0}
                        elif match:
                            f_obj['open'] = match.group()
                            if match_close and round(word_obj_list[idx + 1]['top']) == round(obj['top']):
                                 f_obj['close'] = match_close.group() 
                    except:
                        pass
                    
                continue
  
    df = pd.DataFrame(foia_list)
    st.dataframe(df)