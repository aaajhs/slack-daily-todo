from typing import List
import views
import json
from datetime import datetime, date
import functions

def generate_view(list: List[str], clist: List[str]) -> object:
    list_in_string = functions.list_to_string(list, clist)
    if list_in_string != "":
        views.raw_editor["element"]["initial_value"] = list_in_string
        
    json_object = {
        "type": "home",
        "blocks": [generate_header()] 
            + [generate_list(list, clist)] 
            + [views.add_new_item]
            + [views.divider]
            + [views.raw_editor]
            + [views.submit_raw_edit],
        "external_id": "home_view"
    }
    
    return json.dumps(json_object)
    
def generate_header() -> object:
    header = {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": ":date:  %s  |  %s" % (datetime.today().strftime('%A'), date.today().strftime("%b %d, %Y")),
            "emoji": True
        }
    }
    
    return header
    
def generate_list(list: List[str], clist: List[str]) -> object:

    if clist:
        element = {
            "type": "checkboxes",
            "initial_options": clist,
            "options": list,
            "action_id": "check_item"
        }
    else:
        element = {
            "type": "checkboxes",
            "options": list,
            "action_id": "check_item"
        }
        
        
    list = {
        "type": "actions",
        "elements": [element]
    }
    
    return list

def list_to_string(list: List[str], clist: List[str]) -> str:
    stringified = ""
    for i in list:
        if i in clist:
            stringified += "[x] "
            stringified += i["text"]["text"]
        else:
            stringified += "[ ] "
            stringified += i["text"]["text"]
        stringified += "\n"
        
    return stringified

def string_to_lists(s: str) -> tuple[List[str], List[str]]:
    items_string = s.splitlines()
    items = []
    citems = []
    
    for s in items_string:
        if s == "":
            continue
        
        item = {
            "text": {
                "type": "mrkdwn",
                "text": s[4:],
                "verbatim": False
            },
            "value": s[4:]
        }
        items.append(item)
        
        if s.startswith("[x]"):
            citems.append(item)
            
    return items, citems
