import os
import requests
import json
from bot.discord import bot
from chatterbot.trainers import ListTrainer

MESSAGE_FILE_URL = os.getenv('MESSAGE_FILE_URL')

if __name__ == '__main__':
    message_file = requests.get(MESSAGE_FILE_URL)
    messages = json.loads(message_file.content)

    trainer = ListTrainer(bot)
    trainer.train(messages)
