import random
import re
import string

import emoji

from bot import bot
from keyboards import create_keyboard, keyboards
from models import Game, Tracker, db, User, Poll
from constants import BOT_ID
from actions.host import host_start, host_leave, host_select_roles, host_roles_poll
from actions.player import player_start, player_leave
from actions.utils import generate_users_list, update_users_list

# ------------------------------------
# Connect to database
# ------------------------------------
db.connect()
db.create_tables([Tracker, Game])


def respond_message(message):
    if message.text.startswith('/'):
        return

    message.text = emoji.demojize(message.text)
    t = Tracker.get(Tracker.id == message.chat.id)
    user = User.get(id=message.chat.id)

    # ------------------------------------
    # HOST a game
    # ------------------------------------
    if t.state == 'start' and message.text == ":desktop_computer: Host a Game":
        host_start(message, user)

    # end game
    elif t.state == 'host_game' and message.text == ":cross_mark: Leave":
        host_leave(message, user)

    # select from a list of roles
    elif t.state == 'host_game' and message.text == ":right_arrow: Next":
        host_select_roles(message, user)

    # ------------------------------------
    # New Game
    # ------------------------------------
    elif t.state == 'start' and message.text == ":game_die: Join a Game":
        player_leave(message, user)

    elif t.state == 'join_game':
        player_start(message, user)


def respond_poll(poll):
    host_roles_poll(poll)


