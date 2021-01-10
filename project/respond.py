import random
import re
import string

import emoji

from actions.host import (host_leave, host_roles_poll, host_select_roles,
                          host_select_roles_with_poll, host_send_roles,
                          host_start)
from actions.player import player_leave, player_start
from actions.settings import edit_game_settings
from actions.utils import generate_users_list, update_users_list
from bot import bot
from callbacks.game_settings import respond_game_settings
from callbacks.role_menu import respond_role_menu
from constants import BOT_ID
from finglish import f2p
from keyboards import create_keyboard, keyboards
from models import Game, GameSettings, Poll, Tracker, User, db, RoleSelectionTracker, Role
from utils import send_message, update_state

# ------------------------------------
# Connect to database
# ------------------------------------

def respond_callback(call):
    user = User.get_or_none(id=call.from_user.id)
    if not user:
        send_message(call.from_user.id, ":cross_mark: Not a registered user. Please click on /start.")
        return

    if call.text == ":gear_selector: Game Settings":
        respond_game_settings(call, user)

    elif call.text in [
        "۱. نقش‌های مافیا را انتخاب کنید.",
        "۲. نقش‌های شهروند را انتخاب کنید."
    ]:
        respond_role_menu(call, user)

def respond_message(message):

    if message.text.startswith('/start'):
        register_user(message)


    message.text = emoji.demojize(message.text)
    t = Tracker.get_or_none(Tracker.id == message.chat.id)
    user = User.get_or_none(id=message.chat.id)

    if not t or not user:
        send_message(message.chat.id, ":cross_mark: Not a registered user. Please click on /start.")
        return

    # update the username with every message
    # this is important as it is the only way to find out the user identity
    User.update(
        username=message.chat.username,
    ).where(User.id==message.chat.id).execute()

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
        # FIXME: poll is deactivated. inline keyboard is used now.
        # host_select_roles_with_poll(message, user)
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

    # ------------------------------------
    # Change Name
    # ------------------------------------
    if t.state == 'start' and message.text == ":bust_in_silhouette: Change Name":
        update_state(user, 'change_name')
        text = f":bust_in_silhouette: Current name: <b>{f2p(user.name)}</b>\n\n"
        text += ":input_latin_letters: Enter your new name:"
        send_message(
            user.id,
            text,
            reply_markup=create_keyboard([":cross_mark: Discard"])
        )

    elif t.state == 'change_name' and message.text == ":cross_mark: Discard":
        update_state(user, 'start')
        send_message(user.id, ":cross_mark: Discard", reply_markup=keyboards.main)

    elif t.state == 'change_name':
        if len(message.text) > 100:
            send_message(user.id, "Name length must be less than 100 characters.")
            return

        User.update(name=message.text).where(User.id==user.id).execute()
        update_state(user, 'start')
        send_message(
            user.id,
            f":white_heavy_check_mark: Your Name is updated now to: <b>{message.text}</b>",
            reply_markup=keyboards.main
        )

    # ------------------------------------
    # Settings
    # ------------------------------------
    if t.state == 'start' and message.text == ":gear_selector: Settings":
        edit_game_settings(message, user)


def respond_poll(poll):
    host_roles_poll(poll)


def register_user(message):
    user = User.get_or_none(User.id == message.chat.id)
    if user is not None:
        game = Game.get_or_none(Game.user==user)
        if game is None:
            send_message(
                message.chat.id,
                f"Hi again <b>{user.name}</b>!",
                reply_markup=keyboards.main
            )
        else:
            text = f"Hi again <b>{user.name}</b>!\n\n"
            text += ":game_die: Note that you're in the middle of a game."
            send_message(
                message.chat.id,
                text,
            )

        return False

    send_message(
        message.chat.id,
        f"Hi <b>{message.chat.first_name}</b>!",
        reply_markup=keyboards.main
    )

    # tracker and user information
    Tracker.replace(id=message.chat.id).on_conflict_replace().execute()
    User.replace(
        id=message.chat.id,
        name=message.chat.first_name,
        username=message.chat.username,
    ).on_conflict_replace().execute()

    # default game settings for each user
    user = User.get(User.id == message.chat.id)
    GameSettings.insert(user=user).execute()

    # insert selected roles tracker
    roles = Role.select().where(Role.is_default==True)
    data = []
    for r in roles:
        data.append((r, user, False))
    RoleSelectionTracker.insert_many(
        data, fields=[
            RoleSelectionTracker.role,
            RoleSelectionTracker.user,
            RoleSelectionTracker.checked
        ]
    ).execute()

    return True
