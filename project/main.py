from bot import bot

from keyboards import keyboards
from respond import respond_message
from models import Tracker, User, Game
import emoji
from pprint import pprint
from utils import send_message


# ------------------------------------
# Message Handlers
# ------------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    out_message = send_message(
        message.chat.id,
        f"Hi <b>{message.chat.first_name}</b>!",
        reply_markup=keyboards.main
    )

    tracker_id = (
        Tracker.replace(id=message.chat.id)
        .on_conflict_replace()
        .execute()
    )

    User.replace(
        id=message.chat.id,
        name=message.chat.first_name,
        username=message.chat.username,
        chat_id=out_message.chat.id,
    ).on_conflict_replace().execute()


def handle_messages(messages):
    for message in messages:
        print(emoji.demojize(message.text))
        respond_message(message)


bot.set_update_listener(handle_messages)
# ------------------------------------
print('Running bot...')
bot.polling()
# ------------------------------------
