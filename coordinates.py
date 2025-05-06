coord_list = []
date_obj = {'date_text':"", 'date_x0': "", 'date_top': "", 'date_bottom': ""}
foia_obj = {'foia_text': "", 'foia_x0': "", 'foia_top':"", 'foia_bottom':""}

def coordinates_fun(obj, cat):
    print('in coord list', obj, cat)
    if cat == 'foia':
        foia_obj['foia_text'] = obj['text']
        foia_obj['foia_x0'] = obj['x0']
        foia_obj['foia_top'] = obj['top']
        foia_obj['foia_bottom'] = obj['bottom']
        coord_list.append(foia_obj.copy())
    if cat == 'date':
        date_obj['date_text'] = obj['text']
        date_obj['date_x0'] = obj['x0']
        date_obj['date_top'] = obj['top']
        date_obj['date_bottom'] = obj['bottom']
        coord_list.append(date_obj.copy())
    return coord_list

def coord_list_fun():
    return coord_list