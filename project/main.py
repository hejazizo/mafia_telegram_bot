import re
import sys
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.absolute()
sys.path.append(PROJECT_PATH)

from pprint import pprint

import emoji

from actions.host import host_leave
from actions.player import player_leave, player_start
from bot import bot
from keyboards import keyboards
from models import Game, Tracker, User
from respond import register_user, respond_message, respond_poll
from utils import send_message


# ------------------------------------
# Message Handlers
# ------------------------------------
@bot.poll_answer_handler()
def poll_handler(poll):
    respond_poll(poll)

def handle_messages(messages):
    for message in messages:
        print(emoji.demojize(message.text))
        respond_message(message)

bot.set_update_listener(handle_messages)
# ------------------------------------
print('Running bot...')
bot.polling()
# ------------------------------------
