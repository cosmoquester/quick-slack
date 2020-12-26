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
        json.dump(config, f)


def send_message(token, channel_id, text):
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        json={"channel": channel_id, "text": text},
        headers={"Authorization": f"Bearer {token}"},
    ).json()

    return response
