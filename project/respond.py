import random
import re
import string

import emoji

from actions.host import (host_leave, host_roles_poll, host_select_roles,
                          host_send_roles, host_start)
from actions.player import player_leave, player_start
from actions.utils import generate_users_list, update_users_list
from bot import bot
from constants import BOT_ID
from keyboards import create_keyboard, keyboards
from models import Game, Poll, Tracker, User, db
from utils import send_message

# ------------------------------------
# Connect to database
# ------------------------------------
db.connect()
db.create_tables([Tracker, Game])


def respond_message(message):

    if message.text.startswith('/start'):
        register_user(message)

    message.text = emoji.demojize(message.text)
    t = Tracker.get_or_none(Tracker.id == message.chat.id)
    user = User.get_or_none(id=message.chat.id)

    if not t or not user:
        send_message(message.chat.id, ":cross_mark: Not a registered user. Please click on /start.")
        return

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

    # select from a list of roles
    elif t.state == 'host_game' and message.text == ":envelope: Send Roles":
        host_send_roles(message, user)

    # ------------------------------------
    # New Game
    # ------------------------------------
    join_code_pattern = r"^/start (?P<code>\w{4})$"
    match = re.match(join_code_pattern, message.text)
    if match:
        code = match.group("code")
        message.text = code

    if t.state == 'start' and message.text == ":game_die: Join a Game":
        player_leave(message, user)

    elif t.state == 'join_game':
        player_start(message, user)

    elif t.state == 'start' and match:
        player_start(message, user)


def respond_poll(poll):
    host_roles_poll(poll)


def register_user(message):
    user = User.get_or_none(User.id == message.chat.id)
    if user is not None:
        send_message(
            message.chat.id,
            f"Hi again <b>{message.chat.first_name}</b>!",
        )
        return False

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

    return True