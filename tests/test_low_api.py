from quick_slack.low_api import send_message


def test_send_message():
    response = send_message("xoxb-none", "ABCDEF", "this is some message")

    assert not response["ok"]
    assert response["error"] == "invalid_auth"
