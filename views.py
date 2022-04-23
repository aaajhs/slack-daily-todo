fixed_section=[
    {
        "dispatch_action": True,
        "type": "input",
        "element": {
            "type": "plain_text_input",
            "action_id": "plain_text_input-action"
        },
        "label": {
            "type": "plain_text",
            "text": "Add New Item",
            "emoji": True
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "input",
        "element": {
            "type": "plain_text_input",
            "multiline": True,
            "action_id": "plain_text_input-action"
        },
        "label": {
            "type": "plain_text",
            "text": "Raw Edit",
            "emoji": True
        }
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Click Me",
                    "emoji": True
                },
                "value": "click_me_123",
                "action_id": "actionId-0"
            }
        ]
    }
]