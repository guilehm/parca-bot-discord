import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from discord.ext import commands
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:////tmp/flask_app.db')
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

messages = [
    'oi', 'olá', 'tudo bem?', 'tudo bem!', 'como vai?', 'como foi seu dia?', 'qual seu nome?', 'vamos jogar?',
    'o que você está fazendo?', 'peidei', 'noob', 'eu te amo', 'quantos anos vocẽ tem?', 'eu jogo Fortnite',
    'quantos anos você tem?', 'o que você faz?', 'eu te odeio', 'vaza daqui', 'infeliz', 'idiota', 'desgraça',
    'aff', 'menos, por favor', 'cala a boca', 'fica quieto', 'burro',
]

bot = ChatBot('ParçaBot')
trainer = ListTrainer(bot)
trainer.train(messages)


client = commands.Bot(command_prefix='.')


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


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    client.run(DISCORD_BOT_TOKEN)
