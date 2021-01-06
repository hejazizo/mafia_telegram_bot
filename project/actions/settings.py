from actions import *
from actions.utils import get_game_settings_key_json_data

def edit_game_settings(message, user):
    markup = create_game_settings_keyboard(user)
    out_message = send_message(
        user.id,
        ":gear_selector: Game Settings",
        reply_markup = markup,
    )
    # update message_id for edit
    GameSettings.update(
        message_id=out_message.message_id
    ).where(GameSettings.user==user).execute()

def create_game_settings_keyboard(user):
    game_settings = GameSettings.get(GameSettings.user==user)

    # create keyboard keys
    json_string = get_game_settings_key_json_data(to_string=True)
    for column, value in game_settings.__dict__["__data__"].items():
        if str(value) == "True":
            value = emoji.emojize(":white_heavy_check_mark:")
        if str(value) == "False":
            value = emoji.emojize(":cross_mark:")
        if type(value) == int:
            value = n2p(value)

        # fill data from database
        json_string = json_string.replace(
            f"{{{column}}}", str(value),
        )

    return create_inline_keyboard(json_string)