from quick_slack.utils import load_config, send_message


def test_load_config():
    config = load_config()

    assert config["slack_oauth_token"] == ""
    assert config["default_channel_id"] == ""
    assert config["default_mentions"] == []


def test_send_message():
    response = send_message("xoxb-none", "ABCDEF", "this is some message")

    assert not response["ok"]
    assert response["error"] == "invalid_auth"
