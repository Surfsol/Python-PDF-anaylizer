import streamlit as st
import pdfplumber
import pandas as pd
import io
import re
from datetime import datetime
from coordinates import coordinates_fun
from coordinates import coord_list_fun
#from pdf_parser import parse_pdf_to_table


st.write("Max upload size (MB):", st.get_option("server.maxUploadSize"))

st.title("PDF Data Extraction and Analysis App")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

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

        

        #list to capture coordinates
        coordinate_dict = {
            'foia': 0,
            'open': 0,
            'close': 0
            }
        #find coordinates 

       # 33333 Each page need to run 

        for obj in word_obj_list:
             
             # if the string in obj['text'] begins with 'F-'
             if obj['text'][0] == 'F' and obj['text'][1] == '-':
                
             #save text and coordinate into a list
                if coordinate_dict['foia'] == 0:
                    coordinate_dict['foia'] = obj['x0']
                    coordinates_fun(obj, 'foia')
                elif coordinate_dict['foia'] > obj['x0']:
                    coordinate_dict['foia'] = obj['x0']
                    coordinates_fun(obj, 'foia')
 
            #Dates 
             if obj['x0'] > page.width * .8:
                try:
                    match = re.search(r"\b\d{1,2}/\d{1,2}/\d{4}\b", obj['text'])
                    if match:
                        #print(obj['text'], obj['x0'], obj['x1'])
                        if coordinate_dict['open'] == 0:
                            coordinate_dict['open'] = obj['x0']
                            coordinate_dict['close'] = obj['x1']
                            coordinates_fun(obj, 'date')
                        elif coordinate_dict['open'] > obj['x0']:
                            print('in else if')
                            coordinate_dict['open'] = obj['x0']
                            coordinate_dict['close'] = obj['x1']
                            coordinates_fun(obj, 'date')
                except:
                    continue
        print('77777777777777777777777777777777777', coord_list_fun())
        print(coordinate_dict)
        # coordinate_dict= {'foia': 19.84, 'open': 685.4, 'close': 718.579757588}

    
        for page in pdf.pages:
            #print('width', page.width, page.width * .8)
            text = page.extract_text()
            
            #print('in page', page)
            word_obj_list = page.extract_words()
            f_obj = {'foia':None, 'open': None, 'close': None, 'report': '10/01/2024', 'page': page.page_number}
            for obj in word_obj_list:    
                if abs(obj['x0'] - coordinate_dict['foia']) <= 2:
                    #print('ENTER 1ST AREA', obj['text'], len(obj['text']))
                    if len(obj['text']) > 4 and not obj['text'][0].isdigit():
                        #print('ENTER 1ST AREA 2nd', obj['text'])
                        f_obj['foia'] = obj['text']
                    elif len(obj['text']) == 5 and obj['text'][0].isdigit():
                        #print('before full id', f_obj['foia'], obj['text'], page, obj['x0'] )
                        full_id = f_obj['foia'] + obj['text']
                        f_obj['foia'] = full_id
                        # print('after combine',f_obj)
                        if f_obj['open'] != None:
                            # print('complete', f_obj)
                            foia_list.append(f_obj.copy())
                            #print('After push append', page, foia_list)
                            if f_obj['close'] != None and datetime.strptime(f_obj['report'], "%m/%d/%Y") > datetime.strptime(f_obj['close'], "%m/%d/%Y"):
                                foia_late.append(f_obj.copy())
                            f_obj = {'foia': None, 'open': None, 'close': None, 'report': '10/01/2024', 'page': page.page_number}
                    continue

                elif obj['x0'] >= coordinate_dict['open'] - 2 and obj['x0'] < coordinate_dict['close']:
                    #print('inside open', obj['text'])

                    try:
                        match = re.search(r"\b\d{1,2}/\d{1,2}/\d{4}\b", obj['text'])
                        if match:
                             f_obj['open'] = match.group()
                    except:
                        pass
                    
                elif obj['x0'] >= coordinate_dict['close']:
                    # print('close', coordinate_dict['open'], 'x0', obj['x0'], obj['text'])
                    try:
                        datetime.strptime(obj['text'], "%m/%d/%Y")
                        f_obj['close'] = obj['text']
                        #print('inside close', obj['text'], {f_obj})
                        

                    except:
                        continue
                    
                continue
    dfl = pd.DataFrame(foia_late)
    st.dataframe(dfl)
    df = pd.DataFrame(foia_list)
    st.dataframe(df)
                   


    #     #replace whitespace with underline
    #     text_under = raw_text.replace(' ', '_')
    #     st.text(text_under)
    #     #split at end of line
    #     lines = raw_text.split('\n')
        
    #     for line in lines:
    #             st.text(line)
    #             #if line starts with F- put into a list with 12 items, starting at 0
    #             #in most cases will be 7 items the other 5 will be added later
    #             foia_list =  [None] * 12
    #             if line[0] == 'F' and line[1] == '-':
    #                  f_num_start = line.split()[0]
    #                 # print('f_num',f_num_start)
    #                  st.text(type(line))

    #             #if the row ends in date format, check to see if a date preceeds that date

    #             #ch

    #             columns = re.split(r'\s{2,}', line.strip())
                
    #             if len(columns) >= 1:
    #                 all_rows.append(columns)

    # if all_rows:
    #     # Try to create a DataFrame
    #     try:
    #         df = pd.DataFrame(all_rows)

    #         st.subheader("Extracted Table from PDF (Text Split by Spaces):")
    #         st.dataframe(df)
    #     except Exception as e:
    #         st.error(f"Failed to create table: {e}")
    # else:
    #     st.warning("No table found on the first page.")
