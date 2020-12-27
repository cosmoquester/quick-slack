import click

from .low_api import get_channel_id, get_direct_message_id
from .utils import load_config, modify_config

config = click.Group()


@config.command(help="Show current configs")
def show():
    config = load_config()
    for key, value in config.items():
        click.echo(f"{key:20s}: {str(value) if value else 'None'}")


@config.command("set")
@click.option("--api-token", help="Slack oauth API token start with xoxb-...")
@click.option("--default-mention", help="Default mention users")
@click.option(
    "--default-channel-name",
    help="Default channel name to send message, enter '@username' if channel is direct message",
)
@click.option("--default-channel-id", help="Default channel id to send message")
def set_config(api_token, default_mention, default_channel_name, default_channel_id):
    """
    Set configurations

    Default channel is always only one, so you cannot and don't need to pass default channel name and default channel id.
    """
    if default_channel_name and default_channel_id:
        click.echo("Cannot pass default-channel-name and default-channel-id! default-channel is only one!", err=True)
        exit(1)

    if api_token:
        if not api_token.startswith("xoxb-"):
            click.echo("Slack oauth token is invalid! The token should start with xoxb-...", err=True)
            exit(1)
        modify_config("slack_oauth_token", api_token)
        click.echo("Setting slack token is done.")

    if default_mention:
        default_mention = default_mention.split()
        for mention_user in default_mention:
            if mention_user[0] != "@":
                click.echo("Default mention format is like '@user1 @user2 @user3'. something invalid!", err=True)
                exit(1)
        modify_config("default_mentions", default_mention)
        click.echo("Setting default mentions is done.")

    if default_channel_name:
        if default_channel_name[0] == "@":
            default_channel_id = get_direct_message_id(default_channel_name[1:])
        else:
            default_channel_id = get_channel_id(default_channel_name)
        if not default_channel_id:
            click.echo("Channel name is not valid!", err=True)
            exit(1)

    if default_channel_id:
        modify_config("default_channel_id", default_channel_id)
        click.echo("Setting default channel is done.")


@click.command()
@click.argument("message")
@click.option("-m", "--mention", is_flag=True, help="If use this flag, mention default mention users")
def send(message, mention):
    # TODO: Implement
    pass


@click.command()
@click.argument("command")
@click.option("-s", "--success", help="Message sent if command success")
@click.option("-f", "--fail", help="Message sent if command failed")
@click.option("-m", "--mention", is_flag=True, help="If use this flag, mention default mention users")
def cond(command, success, fail, mention):
    # TODO: Implement
    pass


@click.command()
@click.argument("command")
@click.option("-n", "--interaval", type=click.FLOAT, help="seconds to wait between updates")
@click.option("-m", "--mention", is_flag=True, help="If use this flag, mention default mention users")
def watch(command, interaval, mention):
    # TODO: Implement
    pass


@click.command()
@click.argument("process_id")
@click.argument("message")
@click.option("-m", "--mention", is_flag=True, help="If use this flag, mention default mention users")
def ifexit(process_id, message, mention):
    # TODO: Implement
    pass


if __name__ == "__main__":
    qslack = click.Group(
        "qslack",
        commands={
            "config": config,
            "send": send,
            "cond": cond,
            "watch": watch,
            "ifexit": ifexit,
        },
    )
    qslack()
