from actions import *
from project.utils import edit_message_text

def generate_users_list(game, code, state_info=None):

    response = ":game_die: Mafia Game\n"
    response += f":input_latin_uppercase: Join Code: <code>{code}</code>\n"
    for ind, row in enumerate(game):
        if row.role == 'GOD':
            response += f":smiling_face_with_halo: <b>GOD</b>: {row.user.name} (@{row.user.username})\n\n"
            response += ":busts_in_silhouette: Players\n"
            continue
        response += f"{ind}. {row.user.name} (@{row.user.username}) \n"

    if not state_info:
        state_info = "Waiting for host to accept players..."

    response += "\n"
    response += state_info

    return response

def update_users_list(code):
    game = Game.select().where(
        Game.code==code, Game.state=='start',
    ).order_by(Game.role.asc())
    for ind, row in enumerate(game):
        updated_response = generate_users_list(game, code)
        edit_message_text(updated_response, chat_id=row.user.id, message_id=row.message_id)
