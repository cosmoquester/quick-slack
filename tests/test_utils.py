import json
import os

import pytest

from quick_slack import utils


@pytest.fixture(scope="session")
def config():
    utils.CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "test_config.json")
    return utils.load_config()


@pytest.fixture()
def resource(request):
    def teardown():
        with open(utils.CONFIG_FILE_PATH, "w") as f:
            json.dump({"slack_oauth_token": "", "default_channel_id": "", "default_mentions": []}, f, indent=4)

    request.addfinalizer(teardown)


def test_load_config(resource, config):
    config = utils.load_config()

    assert config["slack_oauth_token"] == ""
    assert config["default_channel_id"] == ""
    assert config["default_mentions"] == []


def test_modify_config(resource, config):
    utils.modify_config("slack_oauth_token", "asdf")
    config = utils.load_config()

    assert config["slack_oauth_token"] == "asdf"
