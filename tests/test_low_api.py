import pytest

from quick_slack import low_api

from .test_utils import config


@pytest.fixture(scope="module")
def psuedo_request():
    class Psuedo:
        def json(self):
            return {
                "ok": True,
                "response_metadata": {"next_cursor": ""},
                "channels": [{"name": "random", "id": "CCCCC", "user": "U23123"}],
                "members": [{"name": "username", "id": "U23123"}, {"name": "username.x", "id": "U123X"}],
                "usergroups": [{"handle": "engineer", "id": "G123123"}],
            }

    low_api.requests.get = lambda *args, **kwargs: Psuedo()
    low_api.requests.post = low_api.requests.get


def test_send_message(config):
    response = low_api.send_message("ABCDEF", "this is some message")

    assert not response["ok"]
    assert response["error"] == "not_authed"


def test_get_channel_id(config):
    with pytest.raises(Exception):
        low_api.get_channel_id("some_channel")


def test_get_user_id(config):
    with pytest.raises(Exception):
        low_api.get_user_id("username")


def test_get_direct_message_id(config):
    with pytest.raises(Exception):
        low_api.get_direct_message_id("username")


def test_get_usergroup_id(config):
    with pytest.raises(Exception):
        low_api.get_usergroup_id("usergroup_handle")


def test_get_channel_id_none(config, psuedo_request):
    assert low_api.get_channel_id("random") == "CCCCC"
    assert low_api.get_channel_id("some_channel") is None


def test_get_user_id_none(config, psuedo_request):
    assert low_api.get_user_id("username") == "U23123"
    assert low_api.get_user_id("username2") is None


def test_get_direct_message_id_none(config, psuedo_request):
    assert low_api.get_direct_message_id("username") == "CCCCC"
    assert low_api.get_direct_message_id("username.x") is None


def test_get_usergroup_id_none(config, psuedo_request):
    assert low_api.get_usergroup_id("engineer") == "G123123"
    assert low_api.get_usergroup_id("usergroup_handle") is None
