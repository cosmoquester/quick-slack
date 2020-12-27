import json
import os

import requests

CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "config.json")


def load_config():
    with open(CONFIG_FILE_PATH) as f:
        config = json.load(f)
    return config


def modify_config(key, value):
    CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "config.json")
    config = load_config()
    config[key] = value

    with open(CONFIG_FILE_PATH, "w") as f:
        json.dump(config, f, indent=4)


def send_message(token, channel_id, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        json={"channel": channel_id, "text": text},
        headers={"Authorization": f"Bearer {token}"},
    ).json()

    return response


def get_channel_id(channel_name):
    config = load_config()

    uri = "https://slack.com/api/conversations.list"
    pararms = {"types": "public_channel,private_channel"}
    prev_id_map = {}
    while True:
        response = requests.get(
            uri, params=pararms, headers={"Authorization": f"Bearer {config['slack_oauth_token']}"}
        ).json()
        id_map = {channel_info["name"]: channel_info["id"] for channel_info in response["channels"]}
        cursor = response["response_metadata"]["next_cursor"]
        pararms["cursor"] = cursor

        if channel_name in id_map:
            return id_map[channel_name]
        elif len(prev_id_map) == len({**prev_id_map, **id_map}):
            return None
        prev_id_map = id_map
