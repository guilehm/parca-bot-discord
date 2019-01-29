import asyncio
import json
import os
import sys
from itertools import cycle

import discord
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

game_list = [
    'Tibia', 'Fortnite', 'CS GO', 'Resident Evil 7', 'Fifa 2019', 'PUBG',
    'o PC pela janela', 'Bosta no Ventilador', 'Lenha na fogueira', 'Meu tempo fora', 'Campo Minado'
]


@client.event
async def on_ready():
    print('Bot está pronto :)')


@client.event
async def on_member_join(member):
    server = member.server
    default_channel = server.default_channel
    await client.send_message(default_channel, 'Olá {}, seja bem-vindo!'.format(member.mention))


@client.event
async def change_status():
    await client.wait_until_ready()
    msgs = cycle(game_list)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(120)


@client.event
async def on_message(message):

    channel = message.channel
    content = message.content

    if content.startswith('.conversar') or content[:3] == '.c ':
        raw_content = message.content.split()
        content = ' '.join(raw_content[1:])
        output = bot.get_response(content)
        await client.send_message(channel, output)

    if content.startswith('.ping'):
        await client.send_message(channel, 'pong! :D')


if __name__ == '__main__':
    client.loop.create_task(change_status())
    client.run(DISCORD_BOT_TOKEN)
