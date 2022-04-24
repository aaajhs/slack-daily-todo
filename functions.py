from typing import List
import views
import json
from datetime import datetime, date

def generate_view(list: List[str], clist: List[str]) -> object:
    json_object = {
        "type": "home",
        "blocks": [generate_header()] + [generate_list(list, clist)] + views.fixed_section,
        "external_id": "home_view"
    }
    # json_object["blocks"] = [generate_header()] + [generate_list(list, clist)] + views.fixed_section
    
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
