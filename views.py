add_new_item = {
    "dispatch_action": True,
    "type": "input",
    "element": {
        "type": "plain_text_input",
        "action_id": "add_new_item"
    },
    "label": {
        "type": "plain_text",
        "text": "Add New Item",
        "emoji": True
    }
}

divider = {"type": "divider"}

raw_editor = {
    "type": "input",
    "element": {
        "type": "plain_text_input",
        "multiline": True,
        "action_id": "raw_editor"
    },
    "label": {
        "type": "plain_text",
        "text": "Raw Edit",
        "emoji": True
    }
}

submit_raw_edit = {
    "type": "actions",
    "elements": [
        {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Submit",
                "emoji": True
            },
            "style": "primary",
            "value": "Submit",
            "action_id": "submit_raw_edit"
        }
    ]
}