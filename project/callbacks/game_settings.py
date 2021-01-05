import json
from pathlib import Path

from actions import ACTIONS_PATH
from actions.settings import create_game_settings_keyboard
from bot import bot
from models import GameSettings
from utils import answer_callback, edit_message_reply_markup, f2p, n2p

SETTINGS_JSON = json.load(open(Path(ACTIONS_PATH, 'settings.json')))

def respond_game_settings(call, user):
    game_settings = GameSettings.get(GameSettings.user==user)

    for section in SETTINGS_JSON["inline_keyboard"]:
        for key in section:
            if call.data != key["callback_data"]:
                continue
            new_value = increase_game_settings_value(
                user, game_settings, call.data, max_value=key["max_value"]
            )

            text = key["text"].format(**{call.data : n2p(new_value)})
            # it is a toggle value
            if key["max_value"] == 1:
                text = key["text"].format(**{call.data : "غیر فعال شد"})
                if new_value:
                    text = key["text"].format(**{call.data : "فعال شد"})

            # send callback
            answer_callback(text, call.id)

    message_id = GameSettings.get(GameSettings.user==user).message_id

    # edit reply keyboard with new values
    edit_message_reply_markup(
        create_game_settings_keyboard(user),
        chat_id=user.id,
        message_id=message_id,
    )

def update_game_settings(user, new_values):
    GameSettings.update(**new_values).where(GameSettings.user==user).execute()

def increase_game_settings_value(user, game_settings, column, max_value=5):
    prev_value = game_settings.__dict__['__data__'][column]
    new_value = prev_value + 1
    if new_value > max_value:
        new_value = 0

    update_game_settings(user, {column: new_value})

    return new_value
