from datetime import datetime
from models import GameSettingsKeys
import pytz

from actions import *
from utils import edit_message_text


def generate_users_list(game, code, state_info=None):
    tz = pytz.timezone('America/Edmonton')
    edmonton_now = datetime.now(tz)

    response = f":game_die: بازی مافیا\n"

    for ind, row in enumerate(game):
        if row.role == "GOD":
            response += f":smiling_face_with_halo: خدا: <b>{f2p(row.user.name)}</b> (@{row.user.username}) \n\n"

            response += ":busts_in_silhouette: بازیکن‌ها\n"
            if len(game) == 1:
                response += "در حال انتظار...\n"
            continue
        response += f"{n2p(ind)}. <b>{f2p(row.user.name)}</b> (@{row.user.username}) \n"

    response += "\n"
    response += "-"*30 + "\n"
    response += f":calendar: {edmonton_now.strftime('%d %B, %Y - %H:%M %Z')}\n"
    response += f":link: Invite Link: https://t.me/Mafianetgame_bot?start={code}\n"
    response += f":input_latin_uppercase: Join Code: <code>{code.upper()}</code>\n\n"

    return response

def update_users_list(code):
    game = Game.select().where(
        Game.code==code, Game.state=='start',
    ).order_by(Game.role.asc())
    for _, row in enumerate(game):
        updated_response = generate_users_list(game, code)
        edit_message_text(updated_response, chat_id=row.user.id, message_id=row.message_id)

def get_game_settings_key_json_data(to_string=False):
    json_data = {
        "inline_keyboard": []
    }
    game_settings_keys = GameSettingsKeys.select().order_by(['row, column'])

    for key in game_settings_keys:
        data = key.__dict__["__data__"]

        # convert True and False to 0 and 1 to avoid json error
        data["is_boolean"] = int(data["is_boolean"])
        if key.column == 0:
            json_data["inline_keyboard"].append([data])
            continue

        json_data["inline_keyboard"][-1].append(data)

    if to_string:
        return str(json_data).replace("'", '"')
    return json_data