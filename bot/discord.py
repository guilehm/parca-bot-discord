import asyncio
import logging
import sys
from itertools import cycle

import discord
import os
import requests
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from discord.ext import commands
from django.db.models.functions import Length

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
from chatterbot.ext.django_chatterbot.models import Statement


RANDOM_MESSAGES = os.getenv('RANDOM_MESSAGES', 1)
RANDOM_MESSAGES_LENGTH = os.getenv('RANDOM_MESSAGES_LENGTH', 50)
RANDOM_MESSAGES_GUILD = os.getenv('RANDOM_MESSAGES_GUILD', 538866016826949653)
RANDOM_MESSAGES_CHANNEL = os.getenv('RANDOM_MESSAGES_CHANNEL', 578037605174738945)
RANDOM_MESSAGES_SLEEP_SECONDS = os.getenv('RANDOM_MESSAGES_SLEEP_SECONDS', 60000)

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

STATEMENTS = Statement.objects.annotate(
    text_len=Length('text')).filter(
    text_len__gt=int(RANDOM_MESSAGES_LENGTH),
).order_by('?')


@client.event
async def on_ready():
    print('Bot está pronto :)')


@client.event
async def change_status():
    await client.wait_until_ready()
    game = cycle(game_list)
    while not client.is_closed():
        current_status = next(game)
        await client.change_presence(activity=discord.Game(current_status))
        await asyncio.sleep(120)


@client.event
async def send_random_messages():
    if RANDOM_MESSAGES:
        await client.wait_until_ready()
        guild = client.get_guild(RANDOM_MESSAGES_GUILD)
        channel = guild.get_channel(RANDOM_MESSAGES_CHANNEL)
        statement = cycle(STATEMENTS)
        while not client.is_closed():
            await channel.send(next(statement).text)
            await asyncio.sleep(int(RANDOM_MESSAGES_SLEEP_SECONDS))


@client.event
async def on_message(message):
    channel = message.channel
    content = message.content

    if content.startswith('.conversar') or content[:3] == '.c ':
        raw_content = message.content.split()
        content = ' '.join(raw_content[1:])
        output = bot.get_response(content)
        await channel.send(output)

    if content.startswith('.ping'):
        await channel.send('pong! :D')


if __name__ == '__main__':
    client.loop.create_task(change_status())
    client.loop.create_task(send_random_messages())
    client.run(DISCORD_BOT_TOKEN)
