import click

config = click.Group()


@config.command()
def show():
    # TODO: Implement
    pass


@config.command("set")
@click.option("--api-token", help="Slack oauth API token start with xoxb-...")
@click.option("--default-mention", help="Default mention users")
@click.option("--default-channel", help="Default channel to send message")
def set_config(api_token, default_mention, default_channel):
    # TODO: Implement
    pass


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
