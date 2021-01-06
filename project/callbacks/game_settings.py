import json
from pathlib import Path

from actions import ACTIONS_PATH
from actions.settings import create_game_settings_keyboard
from bot import bot
from models import GameSettings
from utils import answer_callback, edit_message_reply_markup, f2p, n2p
from actions.utils import get_game_settings_key_json_data


def respond_game_settings(call, user):
    """
    Responds to game settings keys.
    By each click, it either toggles a value or increases it by one.
    """
    game_settings = GameSettings.get(GameSettings.user==user)
    game_settings_key_json = get_game_settings_key_json_data()

    for section in game_settings_key_json["inline_keyboard"]:
        for key in section:
            if call.data != key["callback_data"]:
                continue
            new_value = increase_game_settings_value(
                user, game_settings, call.data, max_value=key["max_value"]
            )

            text = key["text"].format(**{call.data : n2p(new_value)})
            # it is a toggle value
            if key["is_boolean"]:
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

def increase_game_settings_value(user, game_settings, column, max_value=5):
    prev_value = game_settings.__dict__['__data__'][column]
    new_value = prev_value + 1
    if new_value > max_value:
        new_value = 0

    GameSettings.update(**{column: new_value}).where(GameSettings.user==user).execute()
    return new_value
