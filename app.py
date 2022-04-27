import os
from slack_bolt import App
import functions
import pickle
import initialize
from datetime import date, datetime

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
def update_home_tab(client, event, logger, say):
    # TODO load from persistent storage
    
    try:        
        last_message = client.conversations_history(
            channel = event["channel"],
            limit = 1
        )
    
        with open("ilist.dat","rb") as i:
            item_list = pickle.load(i)
        with open("clist.dat","rb") as c:
            checked_item_list = pickle.load(c)
        
        home_view = functions.generate_view(item_list, checked_item_list)
        
        timestamp = int(float(last_message["messages"][0]["ts"]))
        if datetime.fromtimestamp(timestamp).date() != date.today():
            # save status
            message = initialize.save_past_list(item_list, checked_item_list)
            say(message)
            
            # rebuild today's list
            new_list = initialize.listify(message)
            
            with open("ilist.dat", "wb") as i:
                pickle.dump(new_list, i)
            with open("clist.dat", "wb") as c:
                pickle.dump([], c)
            
            home_view = functions.generate_view(new_list, [])
            
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
        
    for j in checked_item_list:
        j["text"]["text"] = functions.cross(j["text"]["text"])
    
    selected_options = action["selected_options"].copy()

    if len(selected_options) > len(checked_item_list):
        for i in selected_options:
            if i in checked_item_list:
                continue
            
            checked_item_list.append(i)
               
    else:
        for i in checked_item_list:
            if i in selected_options:
                continue
            
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

# Start app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))