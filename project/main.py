from bot import bot

from keyboards import keyboards
from respond import respond_message
from models import Tracker, User, Game
import emoji
from pprint import pprint
from utils import send_message
from actions.host import host_leave
from actions.player import player_leave

# ------------------------------------
# Message Handlers
# ------------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):

    user = User.get_or_none(User.id == message.chat.id)
    if user is None:
        send_message(
            message.chat.id,
            f"Hi <b>{message.chat.first_name}</b>!",
            reply_markup=keyboards.main
        )

        Tracker.replace(id=message.chat.id).on_conflict_replace().execute()

        User.replace(
            id=message.chat.id,
            name=message.chat.first_name,
            username=message.chat.username,
        ).on_conflict_replace().execute()

        return

    send_message(
        message.chat.id,
        f"Hi again <b>{message.chat.first_name}</b>!",
    )

@bot.poll_answer_handler()
def pole(pole_result):
    print(pole_result)

def handle_messages(messages):
    for message in messages:
        print(emoji.demojize(message.text))
        respond_message(message)

bot.set_update_listener(handle_messages)
# ------------------------------------
print('Running bot...')
bot.polling()
# ------------------------------------
