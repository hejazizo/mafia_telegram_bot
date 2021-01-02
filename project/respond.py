import emoji
import random
import string

from models import Game, Tracker, db
from bot import bot
from keyboards import keyboards

# ------------------------------------
# Connect to database
# ------------------------------------
db.connect()
db.create_tables([Tracker, Game])


def respond_message(message):
    if message.text.startswith('/'):
        return

    message.text = emoji.demojize(message.text)
    t = Tracker.get(Tracker.username == message.chat.id)
    print(t.state)
    print(message.text)
    print('\n\n')

    if t.state == 'start' and message.text == ":laptop_computer: Host a Game":
        N = 4
        code = ''.join(
            random.choice(
                string.ascii_uppercase
            ) for _ in range(N)
        )
        out_message = bot.send_message(
            message.chat.id,
            emoji.emojize(message.text),
            reply_markup=keyboards.main,
        )
        print(code)
        game_id = (
            Game.replace(
                code=code, username=message.chat.id,
                role='GOD', health_status='Alive',
                message_id=out_message.message_id)
            .on_conflict_replace()
            .execute()
        )

    if t.state == 'start' and message.text == ":game_die: Join a Game":
        response = emoji.emojize(
            ":game_die: Join a Game\n" +
            "Ask your host for the 4-letter game code and enter it here:"
        )
        bot.send_message(
            message.chat.id,
            response,
            reply_markup=keyboards.join_game,
        )
        Tracker.update(state='join_game').where(Tracker.username==t.username).execute()

    if t.state == 'join_game' and message.text == ":BACK_arrow: Back":
        bot.send_message(
            message.chat.id,
            emoji.emojize(message.text),
            reply_markup=keyboards.main,
        )
        Tracker.update(state='start').where(Tracker.username==t.username).execute()

