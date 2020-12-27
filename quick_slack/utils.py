import json
import os
import sys

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
    while True:
        response = requests.get(
            uri, params=pararms, headers={"Authorization": f"Bearer {config['slack_oauth_token']}"}
        ).json()

        if not response["ok"]:
            print(response, file=sys.stderr)
            raise Exception(response["error"])

        pararms["cursor"] = response["response_metadata"]["next_cursor"]

        for channel_info in response["channels"]:
            if channel_name == channel_info["name"]:
                return channel_info["id"]
        if not pararms["cursor"]:
            return None


def get_user_id(username):
    config = load_config()

    uri = "https://slack.com/api/users.list"
    cursor = ""
    while True:
        response = requests.get(
            uri, params={"cursor": cursor}, headers={"Authorization": f"Bearer {config['slack_oauth_token']}"}
        ).json()

        if not response["ok"]:
            print(response, file=sys.stderr)
            raise Exception(response["error"])

        cursor = response["response_metadata"]["next_cursor"]

        for member_info in response["members"]:
            if username == member_info["name"]:
                return member_info["id"]
        if not cursor:
            return None


def get_direct_message_id(username):
    userid = get_user_id(username)

    if userid is None:
        raise Exception(f"user '{username}' is not found!")
    config = load_config()

    uri = "https://slack.com/api/conversations.list"
    pararms = {"types": "im"}
    while True:
        response = requests.get(
            uri, params=pararms, headers={"Authorization": f"Bearer {config['slack_oauth_token']}"}
        ).json()

        if not response["ok"]:
            print(response, file=sys.stderr)
            raise Exception(response["error"])

        pararms["cursor"] = response["response_metadata"]["next_cursor"]

        for channel_info in response["channels"]:
            if userid == channel_info["user"]:
                return channel_info["id"]
        if not pararms["cursor"]:
            return None
