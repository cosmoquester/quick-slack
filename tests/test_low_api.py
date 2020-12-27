from quick_slack import low_api

from .test_utils import config


def test_send_message(config):
    response = low_api.send_message("ABCDEF", "this is some message")

    assert not response["ok"]
    assert response["error"] == "not_authed"
