import json
import os
import sys

import requests
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from discord.ext import commands

from parcaBot.settings import CHATTERBOT, DISCORD_BOT_TOKEN

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parcaBot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

client = commands.Bot(command_prefix='.')
bot = ChatBot(**CHATTERBOT)

MESSAGE_FILE_URL = os.getenv('MESSAGE_FILE_URL')

message_file = requests.get(MESSAGE_FILE_URL)
messages = json.loads(message_file.content)

trainer = ListTrainer(bot)
trainer.train(messages)


@client.event
async def on_ready():
    print('Bot está pronto :)')


@client.event
async def on_message(message):

    channel = message.channel

    if message.content.startswith('.conversar'):
        raw_content = message.content.split()
        content = ' '.join(raw_content[1:])
        output = bot.get_response(content)
        await client.send_message(channel, output)

    if message.content.startswith('.ping'):
        await client.send_message(channel, 'pong! :D')

    if message.content.startswith('.fala'):
        msg = message.content
        output = msg.strip('.fala ')
        await client.send_message(channel, output)


if __name__ == '__main__':
    client.run(DISCORD_BOT_TOKEN)
