from bot import bot

from keyboards import keyboards
from respond import respond_message
from models import Tracker


# ------------------------------------
# Message Handlers
# ------------------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        f"Hi *{message.chat.first_name}*!",
        reply_markup=keyboards.main
    )
    tracker_id = (
        Tracker.replace(username=message.chat.id)
        .on_conflict_replace()
        .execute()
    )

def handle_messages(messages):
    for message in messages:
        respond_message(message)


bot.set_update_listener(handle_messages)
# ------------------------------------
print('Running bot...')
bot.polling()
# ------------------------------------
