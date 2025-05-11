import re




def coord_page(word_obj_list, page):
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
    for obj in word_obj_list:
             # if the string in obj['text'] begins with 'F-'
             if obj['text'].startswith("F-"):
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
             if obj['x0'] > page.width * .05 and obj['x0'] < page.width * .10 and len(obj['text']) > 3:  #.05 = 39.6 and .10 = 79.2
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
    return coordinate_dict