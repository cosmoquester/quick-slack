# Quick slack

[![codecov](https://codecov.io/gh/cosmoquester/quick-slack/branch/master/graph/badge.svg?token=MREUJNXE7L)](https://codecov.io/gh/psj8252/quick-slack)

- CLI tool to send message to mornitor status, notify process end, etc by slack.
- 한국어 README는 [여기](README.ko.md)를 클릭해주세요.

# Install

It is recommended to install using pipx because command might not work depending on virtualenv state.

## Install pipx

```sh
$ python3 -m pip install pipx
```
- see [here](https://github.com/pipxproject/pipx) for more information about installing pipx

## Install Quick Slack for global

```sh
$ pipx install quick-slack
```
After complete the installation of pipx, install Quick-slack through pipx

```
Failing command: ['/home/user/.local/pipx/shared/bin/python3', '-Im', 'ensurepip', '--upgrade', '--default-pip']
'/usr/bin/python3 -m venv --clear /home/user/.local/pipx/shared' failed
```
If an error like above occured, you need to install `python3-venv` or `python3.x-venv` if you installed with commands like `python3.x -m pipx install quick-slack`

## Install Quick Slack for some environment

If you want to install it only in a specific environment, you can install it as a normal pip.
```sh
$ pip install quick-slack
```

# Usage

## Add Bot to workspace

First, go to https://api.slack.com/apps and create an app in Workspace.

Then add the following permissions to the Bot Token Scope:

![Permission](images/image1.png)
![Permission](images/image2.png)

- [chat:write](https://api.slack.com/scopes/chat:write)
- [channels:read](https://api.slack.com/scopes/channels:read)
- [groups:read](https://api.slack.com/scopes/groups:read)
- [im:read](https://api.slack.com/scopes/im:read)
- [mpim:read](https://api.slack.com/scopes/mpim:read)
- [users:read](https://api.slack.com/scopes/users:read)
- [usergroups:read](https://api.slack.com/scopes/usergroups:read)

If you install the app in Workspace from the Install App, you will receive a Bot User OAuth Access Token starting with xoxb.

![Install](images/image3.png)
![Token](images/image4.png)

## Set Config

```sh
$ qslack config
Usage: qslack config [OPTIONS] COMMAND [ARGS]...

  Show or update configs

Options:
  --help  Show this message and exit.

Commands:
  set   Set configurations Default channel is always only one, so you...
  show  Show current configs
```

```
$ qslack config show
slack_oauth_token   : None
default_channel_id  : None
default_mentions    : None
```
'qslack config show' command allows you to view the current config.

```
$ qslack config set --help
Usage: qslack config set [OPTIONS]

  Set configurations

  Default channel is always only one, so you cannot and don't need to pass default channel name and default channel id.
  Default mention format is like '@user1 @here !subteam3'. Warn you should use ! with custom usergroup like 'engineer'.

Options:
  --api-token TEXT             Slack oauth API token start with xoxb-...
  --default-mentions TEXT      Default mention user or groups
  --default-channel-name TEXT  Default channel name to send message, enter
                               '@username' if channel is direct message

  --default-channel-id TEXT    Default channel id to send message
  --help                       Show this message and exit.
```

```
$ qslack config set --api-token xoxb-1231-12312312 --default-mentions '@psj8252 @here' --default-channel-id C10100110
Setting slack token is done.
Setting default mentions is done.
Setting default channel is done.
```
You can set config as shown above
- default-mentions are the target of mention when turning on `mention` option in using the command to send a message.
- default channel means the channel to which a message is sent when using the command to send a message.
- default channel is set by directly entering id as default-channel-id argument or channel name as default-channel-name argument.

## Send Message

```
$ qslack send --help
Usage: qslack send [OPTIONS] MESSAGE

  Send message to the channel

Options:
  -m, --mention            If use this flag, mention default mention
                           user/groups

  -c, --channel-name TEXT  Channel name to send message, use default channel
                           in config if not passed

  --help                   Show this message and exit.
```

You can send message by using `qslack send` command.

```
$ qslack send hi
Error occured in sending message!
{'ok': False, 'error': 'invalid_auth', 'warning': 'missing_charset', 'response_metadata': {'warnings': ['missing_charset']}}
```
If the token is incorrect, the above error may occur.

```
qslack send hi
Error occured in sending message!
{'ok': False, 'error': 'not_in_channel', 'warning': 'missing_charset', 'response_metadata': {'warnings': ['missing_charset']}}
```
- Bot must be added to the channel to send a message. If not, may result in errors such as 'not_in_channel' or 'channel_not_found'.
- If an error occurs, it is related to the slack API, so if you enter the token incorrectly or miss the permission setting, you should set the token properly and add the missing permission.

## Send a message based on command results

```
qslack cond --help
Usage: qslack cond [OPTIONS] COMMAND

  Run command and send message based on whether success command

Options:
  -s, --success TEXT  Message sent if command success
  -f, --fail TEXT     Message sent if command failed
  -m, --mention       If use this flag, mention default mention users
  --help              Show this message and exit.
```
- The command above is to send a message based on the results of the command. If exit code is 0, send the message of success argument and if not, send the message of failure argument.
- If you have not set up a message, do not send a message.

```
$ qslack cond pwd -s hi -f hello
/Users/psj8252/quick-slack
Command success
Sending message is done.
```
For example, if the pwd command is successful, sends a message 'hi'.

```
qslack cond 'bash -c "exit 1"' -f good
Command exit with 1
Sending message is done.
```
In the above case, send the message 'good' because the exit code failed to 1.

## Periodically execute command and send results as a message

```sh
qslack watch --help
Usage: qslack watch [OPTIONS] COMMAND

  Execute command every interval and send message of excution output

Options:
  -n, --interaval FLOAT  seconds to wait between updates
  -m, --mention          If use this flag, mention default mention users
  -s, --silent           If use this flag, ignore output else print output
  -b, --backgroud        Run this command backgroud
  --help                 Show this message and exit.
```
The command above runs the command you enter regularly and sends the result as a message. It can be used like a watch command in linux.

```
$ qslack watch 'sh -c "ls | wc -l"'  -n 3
      13

      13

      13
```
This is an example of how many files in the current directory are monitored every 3 seconds to send messages in a slack.

## Send a message at the end of the currently running process

```
qslack ifend --help
Usage: qslack ifend [OPTIONS] PROCESS_ID MESSAGE

  Check the process is alive in every three seconds and when the process is
  dead, send message

  the process_id is the id of process to mornitor. Warn this command run
  python process as backgroud so can be infinitely running if the process is
  not dead.

Options:
  -m, --mention          If use this flag, mention default mention users
  -n, --interaval FLOAT  seconds to wait between checking liveness
  --help                 Show this message and exit.
```
When you enter a pid, sends a message to the slack at the end of the running process.

```
$ qslack ifend 18103 "end end"
Start mornitoring process 18103...

[+] QuickSlack: Process 18623 end
[+] QuickSlack: Sent message
```
Because it runs as background, if the process does not shut down for a long time, the qslack command remains running.

## Usage in python

```python
$ python3
Python 3.7.3 (v3.7.3:ef4ec6ed12, Mar 25 2019, 16:52:21)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from quick_slack.low_api import send_message

>>> send_message("hihi", mention=True)
{'ok': True, 'channel': 'CCCCCCCCCCC', 'ts': '1609145740.013500', 'message': {'bot_id': 'BBBBBBBBB', 'type': 'message', 'text': '<@UUUUUUU> <!here>\nhihi', 'user': 'U01GEA37VL1', 'ts': '1609145740.013500', 'team': 'TTTTTTTTTT', 'bot_profile': {'id': 'BBBBBBBB', 'deleted': False, 'name': 'Slack CLI', 'updated': 1606963748, 'app_id': 'AAAAAAAAAA', 'icons': {}, 'team_id': 'TTTTTTTTTT'}}, 'warning': 'missing_charset', 'response_metadata': {'warnings': ['missing_charset']}}
>>>
```
You can also use quick_slack in Python as above.
