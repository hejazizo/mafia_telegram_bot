from bot import bot

from keyboards import keyboards
from respond import respond_message, respond_poll, register_user
from models import Tracker, User, Game
import emoji
from pprint import pprint
from utils import send_message
from actions.host import host_leave
from actions.player import player_leave, player_start
import re

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
