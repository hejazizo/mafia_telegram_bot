import random
import re
import string

import emoji

from bot import bot
from keyboards import create_keyboard, keyboards
from models import Game, Tracker, db

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

    # ------------------------------------
    # HOST a game
    # ------------------------------------
    if t.state == 'start' and message.text == ":laptop_computer: Host a Game":
        # generate a 4 digit code (example: DGFH, AQGN, ...)
        N = 4
        code = ''.join(
            random.choice(string.ascii_uppercase) for _ in range(N)
        )

        # generate game message
        out_message = bot.send_message(
            message.chat.id,
            emoji.emojize(message.text),
            reply_markup=keyboards.host_game
        )

        # update game table
        game_id = (
            Game.insert(
                code=code, username=message.chat.id,
                role='GOD', health_status='alive',
                message_id=out_message.message_id)
            .on_conflict('replace')
            .execute()
        )

        # update tracker
        Tracker.update(state='host_game').where(Tracker.username==message.chat.id).execute()

    # end game
    if t.state == 'host_game' and message.text == ":cross_mark: Leave":
        # delete the game
        Game.delete().where(Game.username==message.chat.id)

        # update tracker
        Tracker.update(state='start').where(Tracker.username==message.chat.id).execute()


        # TODO: send message to all participant users.
        bot.send_message(
            message.chat.id,
            emoji.emojize(":cross_mark: Game ended by Host."),
            reply_markup=keyboards.main,
        )

    # ------------------------------------
    # New Game
    # ------------------------------------
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

        # update tracker
        Tracker.update(state='join_game').where(Tracker.username==message.chat.id).execute()

    # back button
    if t.state == 'join_game' and message.text == ":BACK_arrow: Back":
        bot.send_message(
            message.chat.id,
            emoji.emojize(message.text),
            reply_markup=keyboards.main,
        )

        # update tracker
        Tracker.update(state='start').where(Tracker.username==message.chat.id).execute()
