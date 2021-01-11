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
from respond import register_user, respond_message, respond_poll, respond_callback
from utils import send_message
from time import sleep


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

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    call.text = emoji.demojize(call.message.text)
    respond_callback(call)

bot.set_update_listener(handle_messages)
# ------------------------------------
# ------------------------------------

BOT_TOKEN = ""
BOT_INTERVAL = 1
BOT_TIMEOUT = 20

def bot_polling():
    global bot
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex: #Error in polling
            print(f"Bot polling failed, restarting in {BOT_TIMEOUT} sec. Error:\n{ex}")
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: #Clean exit
            bot.stop_polling()
            print("Bot polling loop finished")
            break

print('Running bot...')
bot_polling()