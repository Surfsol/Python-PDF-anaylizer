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
            'name': 0,
            'name_end': 0,
            'open': 0,
            'close': 0,
            'y-range': 0,
            'f_top':0,
            'f_bottom':0,
            'n_top':0,
            'n_bottom':0,
            'd_top':0,
            'd_bottom':0,
            }
        #find coordinates 
        top_y = 0
       # 33333 Each page need to run 

        for obj in word_obj_list:
             # if the string in obj['text'] begins with 'F-'
             if obj['text'][0] == 'F' and obj['text'][1] == '-':
                top_y = obj['top']
                coordinate_dict['f_top'] = obj['top']
                coordinate_dict['f_bottom'] = obj['bottom']
             #save text and coordinate into a list
                if coordinate_dict['foia'] == 0:
                    coordinate_dict['foia'] = obj['x0']
                    #coordinates_fun(obj, 'foia')
                elif coordinate_dict['foia'] > obj['x0']:
                    coordinate_dict['foia'] = obj['x0']
                    #coordinates_fun(obj, 'foia')

             # find y-range
             if coordinate_dict['foia'] != 0 and top_y != 0 and abs(obj['x0'] - coordinate_dict['foia']) < 2 and obj['text'][0].isdigit():
                coordinate_dict['n_top'] = obj['top']
                coordinate_dict['n_bottom'] = obj['bottom']
                dif = obj['bottom'] - top_y
                if coordinate_dict['y-range'] == 0:
                    coordinate_dict['y-range'] = dif
                elif dif < coordinate_dict['y-range']:
                    coordinate_dict['y-range'] = dif
                top_y = 0
                    
            #Name
             if obj['x0'] > page.width * .05 and obj['x0'] < page.width * .10 and len(obj['text']) > 3:
                 if coordinate_dict['name'] == 0:
                     coordinate_dict['name'] = obj['x0']
                     coordinate_dict['name_end'] = obj['x1']
                 elif coordinate_dict['name'] > obj['x0']:
                    coordinate_dict['name'] = obj['x0']
                 elif coordinate_dict['name_end'] < obj['x1']:
                    coordinate_dict['name_end'] = obj['x1']
                    #coordinates_fun(obj, 'name')
                
            #Dates 
             if obj['x0'] > page.width * .8:
                try:
                    match = re.search(r"\b\d{1,2}/\d{1,2}/\d{4}\b", obj['text'])
                    if match:
                        coordinate_dict['d_top'] = obj['top']
                        coordinate_dict['d_bottom'] = obj['bottom']
                        #print(obj['text'], obj['x0'], obj['x1'])
                        if coordinate_dict['open'] == 0:
                            coordinate_dict['open'] = obj['x0']
                            coordinate_dict['close'] = obj['x1']
                            #coordinates_fun(obj, 'date')
                        elif coordinate_dict['open'] > obj['x0']:
                            coordinate_dict['open'] = obj['x0']
                            coordinate_dict['close'] = obj['x1']
                            #coordinates_fun(obj, 'date')
                except:
                    continue
        print('77777777777777777777777777777777777', coord_list_fun())
        print('COORDINATE DICTIONARY',coordinate_dict)
        # coordinate_dict= {'foia': 19.84, 'open': 685.4, 'close': 718.579757588}
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
                        
                        # print('before', date_obj, match_close)
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

        #foia_late
        for item in foia_late:
            page = pdf.pages[item['page'] - 1]

            word_obj_list = page.extract_words()

            # current_items = []
            # for element in foia_late:
            #     if element.page == item.page:
            #         current_items.append(element)
            foia_id = ''
            for obj in word_obj_list:
                # find Foia num
                #if obj['text'][0] == 'F':
                    #print('66666', obj)
                
                if obj['bottom'] > item['top'] and obj['top'] < (item['top'] + 7) and obj['x0'] < coordinate_dict['name'] and obj['text'][0] == 'F' and obj['text'][1] == '-':
                    #print('in FOIA ', obj)
                    foia_id = obj['text']
                if obj['top'] < item['bottom'] and obj['bottom'] < (item['bottom'] + 7) and obj['x0'] < coordinate_dict['name'] and obj['text'][0].isdigit():
                    foia_2 = obj['text']
                    item['foia'] = foia_id + foia_2
                #Name
                if obj['bottom'] < (item['top'] + 13) and obj['top'] < (item['top'] + 7) and obj['x0'] > coordinate_dict['name'] and obj['x0'] > coordinate_dict['name'] and obj['x0'] < coordinate_dict['name_end']:
                    print('NAME', obj['text'])
                    item['name'] = obj['text']

        st.write('Updated Late')
        df_date_late = pd.DataFrame(foia_late)
        st.dataframe(df_date_late)



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
                            
                            # print('complete', f_obj), check to see if close exists
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
                    
                # elif obj['x0'] >= coordinate_dict['close']:
                #     # print('close', coordinate_dict['open'], 'x0', obj['x0'], obj['text'])
                #     try:
                #         datetime.strptime(obj['text'], "%m/%d/%Y")
                #         f_obj['close'] = obj['text']
                #         #print('inside close', obj['text'], {f_obj})
                        

                    # except:
                    #     continue
                    
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
