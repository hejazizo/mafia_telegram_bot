from actions import *
from utils import edit_message_text

def generate_users_list(game, code, state_info=None):

    response = ":game_die: Mafia Game\n"
    response += f":input_latin_uppercase: Join Code: <code>{code}</code>\n\n"

    response += ":busts_in_silhouette: Players\n"
    for ind, row in enumerate(game):
        response += f"{ind+1}. <b>{row.user.name}</b> (@{row.user.username}) \n"

    response += "\n"
    response += ":hourglass_not_done: Waiting for other players to join...\n"
    response += f":link: Invite Link: https://t.me/Mafianetgame_bot?start={code}"

    return response

def update_users_list(code):
    game = Game.select().where(
        Game.code==code, Game.state=='start',
    ).order_by(Game.role.asc())
    for ind, row in enumerate(game):
        updated_response = generate_users_list(game, code)
        edit_message_text(updated_response, chat_id=row.user.id, message_id=row.message_id)
