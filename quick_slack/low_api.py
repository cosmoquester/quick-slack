import sys
from typing import Any, Dict, Optional

import requests

from .utils import load_config


def send_message(text: str, channel_id: Optional[str] = None, mention: bool = False) -> Dict[str, Any]:
    """
    Send text to slack channel

    :param text: (str) message to send
    :param channel_id: (str) the channel id of which send message to channel, default is in config
    :param mention: (bool) if True, mention default mention users and groups else don't

    :return: response Dictionary. refer https://api.slack.com/methods/chat.postMessage for format
    """
    config = load_config()

    if channel_id is None:
        channel_id = config["default_channel_id"]

    if mention:
        text = " ".join(config["default_mentions"]) + "\n" + text

    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        json={"channel": channel_id, "text": text},
        headers={"Authorization": f"Bearer {config['slack_oauth_token']}"},
    ).json()

    return response


def get_channel_id(channel_name: str) -> Optional[str]:
    """
    Get channel id by channel name

    :param channel_name: (str) Channel name ex) random, general
    :return: (str) channel id consisting of numbers and upper case alphabets or None if not foumd
    """
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


def get_user_id(username: str) -> Optional[str]:
    """
    Get user id from username

    :param username: (str) username is used for mention in slack ex) @user1 -> user1 is the username
    :return: (str) user id consisting of numbers and upper case alphabets or None if not foumd
    """
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


def get_direct_message_id(username: str) -> Optional[str]:
    """
    Get Direct message conversation id, it is like get_channel_id but for DMs

    :param username: (str) username is used for mention in slack ex) @user1 -> user1 is the username
    :return: (str) DM channel id consisting of numbers and upper case alphabets or None if not foumd
    """
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


def get_usergroup_id(usergroup_handle: str) -> Optional[str]:
    """
    Get usergroup id, usergroup means custom usergroup like (@product, @engineer, @marketing)
    The names may be also different

    :param usergroup_handle: (str) handler means (product, engineer or marketing) in upper example
    :return: (str) usergroup id
    """
    config = load_config()

    uri = "https://slack.com/api/usergroups.list"
    response = requests.get(uri, headers={"Authorization": f"Bearer {config['slack_oauth_token']}"}).json()

    if not response["ok"]:
        print(response, file=sys.stderr)
        raise Exception(response["error"])

    for usergroup_info in response["usergroups"]:
        if usergroup_handle == usergroup_info["handle"]:
            return usergroup_info["id"]
    return None
