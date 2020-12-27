import click

from .low_api import get_channel_id, get_direct_message_id, get_usergroup_id, send_message
from .utils import load_config, modify_config

config = click.Group()


@config.command(help="Show current configs")
def show():
    config = load_config()
    for key, value in config.items():
        click.echo(f"{key:20s}: {str(value) if value else 'None'}")


@config.command("set")
@click.option("--api-token", help="Slack oauth API token start with xoxb-...")
@click.option("--default-mentions", help="Default mention user or groups")
@click.option(
    "--default-channel-name",
    help="Default channel name to send message, enter '@username' if channel is direct message",
)
@click.option("--default-channel-id", help="Default channel id to send message")
def set_config(api_token, default_mentions, default_channel_name, default_channel_id):
    """
    Set configurations

    \b
    Default channel is always only one, so you cannot and don't need to pass default channel name and default channel id.
    Default mention format is like '@user1 @here !subteam3'. Warn you should use ! with custom usergroup like 'engineer'.
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

    if default_mentions:
        default_mention_list = []
        for mention_user in default_mentions.split():
            # Special Group
            if mention_user in ("@here", "@channel", "@everyone"):
                default_mention_list.append(f"<{mention_user.replace('@', '!')}>")
            # User
            elif mention_user[0] == "@":
                default_mention_list.append(f"<{mention_user}>")
            # Subteam
            elif mention_user[0] == "!":
                subteam_id = get_usergroup_id(mention_user[1:])
                if not subteam_id:
                    click.echo(f"Subteam '{mention_user[1:]}' is not found!", err=True)
                    exit(1)
                default_mention_list.append(f"<!subteam^{subteam_id}>")
            else:
                click.echo("Default mention format is like '@user1 @here !subteam3'. something invalid!", err=True)
                exit(1)

        modify_config("default_mentions", default_mention_list)
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
@click.option("-c", "--channel-name", help="Channel name to send message, use default channel in config if not passed")
def send(message, mention, channel_name):
    """
    Send message to the channel
    """
    config = load_config()

    if channel_name:
        if channel_name[0] == "@":
            channel_id = get_direct_message_id(channel_name[1:])
        else:
            channel_id = get_channel_id(channel_name)
        if not channel_id:
            click.echo("Channel name is not valid!", err=True)
            exit(1)
    else:
        channel_id = config["default_channel_id"]

    if mention:
        message = " ".join(config["default_mentions"]) + "\n" + message

    response = send_message(config["slack_oauth_token"], channel_id, message)
    if not response["ok"]:
        click.echo("Error occured in sending message!", err=True)
        click.echo(str(response), err=True)
        exit(1)
    click.echo("Done.")


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
