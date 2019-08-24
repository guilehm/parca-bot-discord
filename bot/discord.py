import asyncio
import logging
import os
import sys
from itertools import cycle

import discord
import requests
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from discord.ext import commands

from parcaBot.settings import CHATTERBOT, DISCORD_BOT_TOKEN, DARK_SOULS_ENDPOINT

logger = logging.getLogger(__name__)

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

from bot.models import WakeUp
client = commands.Bot(command_prefix='.')
bot = ChatBot(
    **CHATTERBOT,
    response_selection_method=get_random_response,
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "response_selection_method": "chatterbot.response_selection.get_random_response"
        }
    ]
)

game_list = [
    'Tibia', 'Bosta no Ventilador', 'Fortnite', 'CS GO', 'Fifa 2019', 'PUBG', 'Meu cachorro na piscina',
    'o PC pela janela', 'Lenha na fogueira', 'Meu tempo fora', 'Campo Minado', 'Minha irmã no chão',
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

    if content.startswith('.acordar'):
        wake_message = 'Tentando acordar o Dark BOT'
        await client.send_message(channel, wake_message)
        r = requests.get(DARK_SOULS_ENDPOINT)
        try:
            WakeUp.objects.create(data=r.json())
            output = 'Acho que consegui acordá-lo'
        except Exception as e:
            output = f'Não consegui acordar o Dark BOT \n {e}'
            logger.exception(e, exc_info=True)

        await client.send_message(channel, output)


if __name__ == '__main__':
    client.loop.create_task(change_status())
    client.run(DISCORD_BOT_TOKEN)
