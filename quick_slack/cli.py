import click

from .utils import load_config, modify_config

config = click.Group()


@config.command(help="Show current configs")
def show():
    config = load_config()
    for key, value in config.items():
        click.echo(f"{key:20s}: {str(value) if value else 'None'}")


@config.command("set", help="Set config")
@click.option("--api-token", help="Slack oauth API token start with xoxb-...")
@click.option("--default-mention", help="Default mention users")
@click.option("--default-channel", help="Default channel to send message")
def set_config(api_token, default_mention, default_channel):
    configs = {}
    if api_token:
        if not api_token.startswith("xoxb-"):
            click.echo("Slack oauth token is invalid! The token should start with xoxb-...", err=True)
            exit(1)
        configs["slack_oauth_token"] = api_token

    if default_mention:
        default_mention = default_mention.split()
        for mention_user in default_mention:
            if mention_user[0] != "@":
                click.echo("Default mention format is like '@user1 @user2 @user3'. something invalid!", err=True)
                exit(1)
        configs["default_mentions"] = default_mention

    if default_channel:
        configs["default_channel_id"] = default_channel

    if not configs:
        click.echo("Please input parameter and value!", err=True)
        exit(1)

    for key, value in configs.items():
        modify_config(key, value)
    click.echo("Done.")


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
