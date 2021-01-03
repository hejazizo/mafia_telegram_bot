import os

import telebot
#------------------------------------
# You can set parse_mode by default.
# HTML or MARKDOWN
# ------------------------------------
bot = telebot.TeleBot(
    os.getenv('mafia_telegram_bot'), parse_mode="HTML"
)