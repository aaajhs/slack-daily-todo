from datetime import datetime, date, timedelta
from typing import List

def save_past_list(ilist: List[str], clist: List[str]) -> str:
    yesterday = date.today() - timedelta(days = 1)
    message = "*~ %s*\n" % (yesterday.strftime("%b %d, %Y"))
    message += stringify(ilist, clist)
    
    return message

def stringify(ilist: List[str], clist: List[str]) -> str:
    list = ""
    
    for i in ilist:
        if i in clist:
            message = "• ~%s~" % i["value"]
        else:
            message = "• %s" % i["value"]
        message += "\n"
        list += message
    
    return list

def listify(s: str) -> List[str]:
    items_string = s.splitlines()
    items_string.pop(0)
    
    items = []
    
    for i in items_string:
        if i == "" or i.startswith("• ~"):
            continue
           
        item = {
            "text": {
                "type": "mrkdwn",
                "text": i[2:],
                "verbatim": False
            },
            "value": i[2:]
        }
        items.append(item)
    return items
