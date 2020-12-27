from quick_slack.utils import load_config


def test_load_config():
    config = load_config()

    assert config["slack_oauth_token"] == ""
    assert config["default_channel_id"] == ""
    assert config["default_mentions"] == []
