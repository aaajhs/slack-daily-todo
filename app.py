import os
from slack_bolt import App
import functions
import pickle

app = App(
    token = os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET"),
)

# item_list = [
#     {
#         "text": {
#             "type": "mrkdwn",
#             "text": "option 0",
#             "verbatim": False
#         },
#         "value": "value-0"
#     },
#     {
#         "text": {
#             "type": "mrkdwn",
#             "text": "option 1",
#             "verbatim": False
#         },
#         "value": "value-1"
#     },
#     {
#         "text": {
#             "type": "mrkdwn",
#             "text": "option 2",
#             "verbatim": False
#         },
#         "value": "value-2"
#     }
# ]

# checked_item_list = []

# Handle interactions
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    
    # TODO load from persistent storage
    with open("ilist.dat","rb") as i:
        item_list = pickle.load(i)
    with open("clist.dat","rb") as c:
        checked_item_list = pickle.load(c)
    
    try:        
        home_view = functions.generate_view(item_list, checked_item_list)
        client.views_publish(
            user_id = event["user"],
            view=home_view
        )
  
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

@app.action("check_item")
def handle_checked_item(ack, action, client):
    ack()
    
    # TODO save to persistent storage
    with open("ilist.dat","rb") as i:
        item_list = pickle.load(i)
    with open("clist.dat","rb") as c:
        checked_item_list = pickle.load(c)
    
    selected_options = action["selected_options"].copy()

    if len(selected_options) > len(checked_item_list):
        for i in selected_options:
            if i in checked_item_list:
                continue
            
            if not i["text"]["text"].startswith('~') and not i["text"]["text"].endswith('~'):
                newstring = "~%s~" % i["text"]["text"]
                item_list[item_list.index(i)]["text"]["text"] = newstring
                i["text"]["text"] = newstring
            
                checked_item_list.append(i)
               
    else:
        for i in checked_item_list:
            if i in selected_options:
                continue
            
            if i["text"]["text"].startswith('~') and i["text"]["text"].endswith('~'):
                newstring = i["text"]["text"][1:-1]
                item_list[item_list.index(i)]["text"]["text"] = newstring
                i["text"]["text"] = newstring
            
                checked_item_list.remove(i)
    
    # TODO load from persistent storage
    with open("ilist.dat","wb") as i:
        pickle.dump(item_list, i)
    with open("clist.dat","wb") as c:
        pickle.dump(checked_item_list, c)
    
    client.views_update(
        external_id="home_view",
        view=functions.generate_view(item_list, checked_item_list)
    )

@app.action("add_new_item")
def approve_request(ack, action, client):
    ack()
    
    newitem = {
        "text": {
            "type": "mrkdwn",
            "text": action["value"],
            "verbatim": False
        },
        "value": action["value"]
    }
    
    with open("ilist.dat","rb") as i:
        item_list = pickle.load(i)
    with open("clist.dat","rb") as c:
        checked_item_list = pickle.load(c)
        
    item_list.append(newitem)
        
    with open("ilist.dat","wb") as i:
        pickle.dump(item_list, i)
    
    client.views_update(
        external_id="home_view",
        view=functions.generate_view(item_list, checked_item_list)
    )

@app.action("actionId-0")
def approve_request(ack, say, client):
    # TODO Update entire list
    ack()
    say(channel="U02940L9DEX", text="Request approved 👍")

    client.views_update(
        external_id="home_view",
        view=functions.check_item(item_list)
    )

# Start app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))