import re
import sys
from pathlib import Path

PROJECT_PATH = Path(__file__).parent.absolute()
sys.path.append(PROJECT_PATH)

import logging
import sys
from pprint import pprint

from constants import DEFAULT_LOG_LEVEL, BOT_INTERVAL, BOT_TIMEOUT
from utils import configure_colored_logging

logger = logging.getLogger(__name__)

from time import sleep

import emoji

from actions.host import host_leave
from actions.player import player_leave, player_start
from bot import bot
from keyboards import keyboards
from models import Game, Tracker, User
from respond import (register_user, respond_callback, respond_message,
                     respond_poll)
from utils import create_argument_parser, send_message


# ------------------------------------
# Message Handlers
# ------------------------------------
@bot.poll_answer_handler()
def poll_handler(poll):
    respond_poll(poll)

def handle_messages(messages):
    for message in messages:
        logger.info(f"User Input --> {message.text}")
        respond_message(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    call.text = emoji.demojize(call.message.text)
    logger.info(f"User Callback --> {call.text}")
    respond_callback(call)

bot.set_update_listener(handle_messages)
# ------------------------------------
# ------------------------------------

def bot_polling():
    global bot
    logger.info("Starting bot polling now")
    while True:
        try:
            logger.info("New bot instance started")
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex: #Error in polling
            logger.warning(f"Bot polling failed, restarting in {BOT_TIMEOUT} sec. Error:\n{ex}")
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: #Clean exit
            bot.stop_polling()
            logger.error("Bot polling loop finished")
            break


if __name__ == "__main__":
    arg_parser = create_argument_parser()
    cmdline_arguments = arg_parser.parse_args()
    log_level = cmdline_arguments.loglevel if hasattr(cmdline_arguments, "loglevel") else None

    if not log_level:
        log_level = DEFAULT_LOG_LEVEL

    logging.getLogger("main").setLevel(log_level)
    configure_colored_logging(log_level)

    bot_polling()
