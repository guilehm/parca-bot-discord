from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from django.http import JsonResponse

from parcaBot.settings import CHATTERBOT

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


def answer(request):
    response = dict(succes=True)
    if request.method == 'POST':
        question = request.POST['question']
        response = dict(answer=bot.get_response(question).text)
    return JsonResponse(response)
