import json
from pathlib import Path

from bitbitbot import command
from bitbitbot.bot import BitBitBot
from bitbitbot.models import Role, TwitchTags
from pydantic import parse_raw_as

from .models import Command

plugin_path = Path(__file__).parent
responses_file = plugin_path / 'responses.json'


def sender_factory(message):
    def _wrapped(bot: BitBitBot, msg: str, tags: TwitchTags):
        args = msg.split()

        try:
            formatted_message = message.format(*args)
        except Exception as e:
            print(e)
            return

        bot.send_message(formatted_message)
    return _wrapped


def load_commands(command_list):
    for cmd in command_list:
        command(cmd.name, cmd.permission)(sender_factory(cmd.message))

def save_commands(command_list):
    with open(responses_file, 'w+') as f:
        f.write(
            json.dumps(
                [
                    command.dict()
                    for command in command_list
                ],
                sort_keys=True,
                indent=4
            )
        )


@command('add_command', Role.MODERATOR)
def add_command(bot: BitBitBot, msg: str, tags: TwitchTags):
    command_name, *message = msg.split()
    command_name = command_name.lower()
    message = ' '.join(message)

    with open(responses_file, 'r') as f:
        command_list = parse_raw_as(list[Command], f.read())

    new_command = Command(name=command_name, message=message)
    command_list.append(new_command)

    save_commands(command_list)
    load_commands(command_list)
    bot.send_message(f'Command {new_command.name} added successfully!')

@command('set_permission', Role.MODERATOR)
def set_permission(bot: BitBitBot, msg: str, tags: TwitchTags):
    try:
        command_name, permission_level = msg.split()
        command_name = command_name.lower()
        permission_level = permission_level.upper()
        role = Role[permission_level]
    except (ValueError, KeyError):
        return

    with open(responses_file, 'r') as f:
        command_list = parse_raw_as(list[Command], f.read())

    for cmd in command_list:
        if cmd.name == command_name:
            cmd.permission = role
            save_commands(command_list)
            load_commands(command_list)
            bot.send_message(f'Permissions updated for command {cmd.name} successfully!')
            return


try:
    with open(responses_file, 'r') as f:
        command_list = parse_raw_as(list[Command], f.read())
except FileNotFoundError:
    save_commands([])
    command_list = []

load_commands(command_list)
