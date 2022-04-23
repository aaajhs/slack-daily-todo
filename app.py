import os
from slack_bolt import App
import views
import json
import functions
import pickle

app = App(
    token = os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET"),
)

# TODO get list from slack message or db
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
    
    with open("ilist.dat","rb") as i:
        item_list = pickle.load(i)
    with open("clist.dat","rb") as c:
        checked_item_list = pickle.load(c)
    
    try:        
        # TODO Build view dynamically
        home_view = functions.generate_view(item_list, checked_item_list)
        client.views_publish(
            user_id = event["user"],
            view=home_view
        )
  
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

@app.action("check_item")
def handle_some_action(ack, action, client):
    ack()
    
    with open("ilist.dat","rb") as i:
        item_list = pickle.load(i)
    with open("clist.dat","rb") as c:
        checked_item_list = pickle.load(c)
    
    # if checked_item_list - action["selected_options"] != []: # 새로 추가된게 더 많은 경우 = 새로 추가된걸 텍스트 바꾸고 checked_item_list에 추가
    #     delta = action["selected_options"] - checked_item_list
    # elif action["selected_options"] - checked_item_list != []: # 기존에 있던게 더 많다 = 뭔가가 빠졌다
    #     delta = checked_item_list - action["selected_options"]
    

    
    checked_item_list = action["selected_options"].copy()
    
    
    # for i in checked_item_list:
    #     print(i["text"]["text"][1:-1])
    #     if i["text"]["text"].startswith('~') and i["text"]["text"].endswith('~'):
    #         newstring = i["text"]["text"][1:-1]
    #         item_list[item_list.index(i)]["text"]["text"] = newstring
    #         i["text"]["text"] = newstring
    #     else:
    #         newstring = "~%s~" % i["text"]["text"]
    #         item_list[item_list.index(i)]["text"]["text"] = newstring
    #         i["text"]["text"] = newstring
    
    
    
            
                
    
    with open("ilist.dat","wb") as i:
        pickle.dump(item_list, i)
    with open("clist.dat","wb") as c:
        pickle.dump(checked_item_list, c)
    
    # print(item_list)
    # print(checked_item_list)
    # print(action["selected_options"])
    client.views_update(
        external_id="home_view",
        view=functions.generate_view(item_list, checked_item_list)
    )
                

@app.action("plain_text_input-action")
def approve_request(ack, say):
    # TODO Add item to list
    ack()
    say(channel="U02940L9DEX", text="Request approved 👍")

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