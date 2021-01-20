import json
from pathlib import Path

from bitbitbot import command
from bitbitbot.bot import BitBitBot
from bitbitbot.models import TwitchTags

plugin_path = Path(__file__).parent
responses_file = plugin_path / 'responses.json'

try:
    with open(responses_file, 'r') as f:
        pass
except FileNotFoundError:
    with open(responses_file, 'w+') as f:
        f.write(json.dumps({}))


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


def load_commands(command_dict=None):
    if command_dict is None:
        with open(responses_file, 'r') as f:
            command_dict = json.loads(f.read())

    for name, message in command_dict.items():
        command(name)(sender_factory(message))


@command('add_command')
def add_command(bot: BitBitBot, msg: str, tags: TwitchTags):
    if tags.display_name.lower() != bot.channel.lower()[1:]:
        return

    command_name, *message = msg.split()
    command_name = command_name.lower()
    message = ' '.join(message)

    with open(responses_file, 'r') as f:
        command_dict = json.loads(f.read())

    command_dict[command_name] = message

    with open(responses_file, 'w+') as f:
        f.write(json.dumps(command_dict, sort_keys=True, indent=4))

    load_commands(command_dict)
    bot.send_message(f'Command {command_name} added successfully!')


load_commands()
