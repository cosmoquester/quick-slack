# Quick slack

[![codecov](https://codecov.io/gh/psj8252/quick-slack/branch/master/graph/badge.svg?token=MREUJNXE7L)](https://codecov.io/gh/psj8252/quick-slack)

- 빠르게 slack 메세지를 보내는 cli툴입니다. 프로세스 종료 알림, 실행 결과에 따라 알림 등의 기능을 지원합니다.

# Install

그냥 설치하면 virtualenv 상태에 따라 command가 동작하지 않을 수 있기 때문에 pipx를 이용해 설치하기를 권장합니다.

pipx로 설치할 경우 virtualenv 상태와 상관없이 명령어를 사용할 수 있습니다. 먼저 pipx를 설치합니다.

## Install pipx

```sh
$ python3 -m pip install pipx
```
- pipx의 설치에 대한 자세한 내용은 [여기](https://github.com/pipxproject/pipx)를 참고해주세요.

## Install Quick Slack for global

```sh
$ pipx install quick-slack
```
pipx의 설치를 완료하면 pipx를 통해 quick-slack을 설치합니다.

## Install Quick Slack for some environment

만약 특정 환경에만 설치하고 싶다면 평범하게 pip로 설치하면 됩니다.
```sh
$ pip install quick-slack
```

# Usage

## Slack에 Bot 추가하기

먼저 https://api.slack.com/apps 에 들어가서 Workspace에 App을 만들어줍니다.

그 다음 Bot Token Scope에 아래의 권한을 추가해줍니다.

![Permission](images/image1.png)
![Permission](images/image2.png)

- [chat:write](https://api.slack.com/scopes/chat:write)
- [channels:read](https://api.slack.com/scopes/channels:read)
- [groups:read](https://api.slack.com/scopes/groups:read)
- [im:read](https://api.slack.com/scopes/im:read)
- [mpim:read](https://api.slack.com/scopes/mpim:read)
- [users:read](https://api.slack.com/scopes/users:read)
- [usergroups:read](https://api.slack.com/scopes/usergroups:read)

그리고 Install App 에서 Workspace에 App을 Install하면 xoxb로 시작하는 Bot User OAuth Access Token을 발급받습니다.

![Install](images/image3.png)
![Token](images/image4.png)

## Config 설정

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
`qslack config show` 명령어를 통해 현재 config를 볼 수 있습니다.

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
위와 같은 방식으로 설정할 수 있습니다.
- default-mentions는 메세지를 보내는 명령어를 사용할 때 mention 옵션을 켤 경우 mention이 되는 대상입니다.
- default channel은 메세지를 보내는 명령어를 사용할 때 메세지가 보내지는 채널을 의미합니다.
- default channel은 default-channel-id 인자로 id를 직접 입력하거나 default-channel-name 인자로 channel이름을 입력해 설정합니다.

## 메세지 보내기

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

qslack send 명령어로 채널에 메시지를 보낼 수 있습니다.

```
$ qslack send hi
Error occured in sending message!
{'ok': False, 'error': 'invalid_auth', 'warning': 'missing_charset', 'response_metadata': {'warnings': ['missing_charset']}}
```
token이 올바르지 않을 경우 위와같은 에러가 발생할 수 있습니다.

```
qslack send hi
Error occured in sending message!
{'ok': False, 'error': 'not_in_channel', 'warning': 'missing_charset', 'response_metadata': {'warnings': ['missing_charset']}}
```
- Bot이 메세지를 보내기 위해서는 해당 채널에 들어와 있어야 합니다. 그렇지 않으면 `'not_in_channel'`, `'channel_not_found'` 등의 에러가 날 수 있습니다.
- 에러가 나는 경우는 slack API와 관련된 부분이니 토큰을 잘못 입력했거나 권한설정을 빼먹은 경우 토큰을 제대로 설정하고 빠진 권한을 추가하는 등의 조치를 취해주시면 됩니다.

## 명령어 결과에 따라 메세지 보내기

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
- 위 명령어는 command의 실행결과에 따라 메세지를 보내는 명령어 입니다. exit code가 0이면 success인자로 받은 메세지를 보내고 0이 아니면 fail인자로 받은 메세지를 보냅니다.
- 메세지를 설정하지 않은 경우에는 따로 메세지를 보내지 않습니다.

```
$ qslack cond pwd -s hi -f hello
/Users/psj8252/quick-slack
Command success
Sending message is done.
```
예들들어 이렇게 pwd명령을 성공하면 hi라는 메세지를 보냅니다.

```
qslack cond 'bash -c "exit 1"' -f good
Command exit with 1
Sending message is done.
```
위 경우에는 exit코드가 1로 실패했기 때문에 good이라는 메세지를 보냅니다.

## 주기적으로 명령어를 실행하고 결과를 메세지로 보내기

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
위 명령어는 입력한 command를 정기적으로 실행하여 그 결과를 메세지로 전송합니다. watch 명령어처럼 사용할 수 있습니다.

```
$ qslack watch 'sh -c "ls | wc -l"'  -n 3
      13

      13

      13
```
현재 디렉토리의 파일 개수를 3초마다 모니터링하여 슬랙으로 메세지를 보내주는 예시입니다.

## 현재 실행 중인 프로세스가 끝나면 메세지를 전송

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
pid를 입력하면 실행중인 프로세스가 끝났을 때 슬랙으로 메세지를 전송하는 명령어입니다.

```
$ qslack ifend 18103 "end end"
Start mornitoring process 18103...

[+] QuickSlack: Process 18623 end
[+] QuickSlack: Sent message
```
이 명렁어는 background로 실행되기 때문에 해당 프로세스가 오랫동안 종료되지 않을 경우 qslack command가 계속 실행 중인 상태로 유지됩니다.

## Python에서 사용하기

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
파이썬에서도 위와 같이 사용할 수는 있습니다.
