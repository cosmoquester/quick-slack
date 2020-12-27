import json
import os

from click.testing import CliRunner

from quick_slack import cli, low_api, utils
from quick_slack.cli import qslack


class TestCLI:
    @classmethod
    def setup_class(cls):
        cls.runner = CliRunner()
        cls.qslack = qslack

        # Mock
        utils.CONFIG_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "test_config.json")
        cli.get_usergroup_id = lambda x: "U10101010"
        cli.get_direct_message_id = lambda x: "dmdm.hihi"
        cli.get_channel_id = lambda x: "C12345"
        cli.send_message = lambda *args, **kwargs: {"ok": True}

    @classmethod
    def teardown_class(cls):
        with open(utils.CONFIG_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump({"slack_oauth_token": "", "default_channel_id": "", "default_mentions": []}, f, indent=4)

        cli.get_usergroup_id = low_api.get_usergroup_id
        cli.get_direct_message_id = low_api.get_direct_message_id
        cli.get_channel_id = low_api.get_channel_id
        cli.send_message = low_api.send_message

    def test_help(self):
        assert self.runner.invoke(self.qslack, ["--help"]).exit_code == 0

    def test_config(self):
        # fmt: off
        assert self.runner.invoke(self.qslack, ["config", "--help"]).exit_code == 0

        assert self.runner.invoke(self.qslack, ["config", "show"]).exit_code == 0
        assert self.runner.invoke(self.qslack, ["config", "show", "ababebebe"]).exit_code != 0

        assert self.runner.invoke(self.qslack, ["config", "set", "--api-token", "abebebe"]).exit_code != 0
        assert self.runner.invoke(self.qslack, ["config", "set", "--api-token", "xoxb-1234-55"]).exit_code == 0

        assert self.runner.invoke(self.qslack, ["config", "set", "--default-mentions", "@hi #hello"]).exit_code != 0
        assert self.runner.invoke(self.qslack, ["config", "set", "--default-mentions", "@hi @here !group1"]).exit_code == 0

        assert self.runner.invoke(self.qslack, ["config", 'set', '--default-channel-name', 'some', '--default-channel-id', 'good']).exit_code != 0
        assert self.runner.invoke(self.qslack, ["config", 'set', '--default-channel-name', 'some']).exit_code == 0
        assert self.runner.invoke(self.qslack, ["config", 'set', '--default-channel-name', '@gooduser']).exit_code == 0
        assert self.runner.invoke(self.qslack, ["config", 'set', '--default-channel-id', 'CCCC']).exit_code == 0
        # fmt: on

        assert utils.load_config() == {
            "slack_oauth_token": "xoxb-1234-55",
            "default_mentions": ["<@hi>", "<!here>", "<!subteam^U10101010>"],
            "default_channel_id": "CCCC",
        }

    def test_send(self):
        assert self.runner.invoke(self.qslack, ["send", "--help"]).exit_code == 0

        cli.get_channel_id = lambda x: None
        assert self.runner.invoke(self.qslack, ["send", "hihi", "-c", "adfasdf"]).exit_code != 0
        assert self.runner.invoke(self.qslack, ["send", "hihi", "-c", "@adfasdf"]).exit_code == 0
        assert self.runner.invoke(self.qslack, ["send", "hihi", "-m"]).exit_code == 0
        cli.send_message = lambda *args, **kwargs: {"ok": False}
        assert self.runner.invoke(self.qslack, ["send", "hihi", "-m"]).exit_code == 1

    def test_cond(self):
        assert self.runner.invoke(self.qslack, ["cond", "--help"]).exit_code == 0

        result = self.runner.invoke(self.qslack, ["cond", "pwd", "-s", "good"])
        assert result.exit_code == 0
        assert result.output == "Command success\n"

        result = self.runner.invoke(self.qslack, ["cond", "pwd", "-f", "bad", "-m"])
        assert result.exit_code == 0
        assert result.output == ""

        result = self.runner.invoke(self.qslack, ["cond", "bash -c 'exit 1'", "-f", "bad"])
        assert result.exit_code == 0
        assert result.output == "Command failed\n"

    def test_watch(self):
        assert self.runner.invoke(self.qslack, ["watch", "--help"]).exit_code == 0

    def test_ifend(self):
        assert self.runner.invoke(self.qslack, ["ifend", "--help"]).exit_code == 0
