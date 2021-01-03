from actions import *
from project.actions.utils import generate_users_list

def host_start(message, user):
    # generate a 4 digit code (example: DGFH, AQGN, ...)
    N = 4
    code = ''.join(
        random.choice(string.ascii_uppercase) for _ in range(N)
    )

    # update game table
    Game.replace(
        user=user,
        id=user.id,
        code=code,
        role='GOD', health_status='alive',
        state='start',
    ).on_conflict('replace').execute()

    game = Game.select().where(
        Game.code==code, Game.state=='start'
    ).order_by(Game.role.asc())

    # generate game message
    response = generate_users_list(game, code)
    out_message = send_message(
        message.chat.id,
        emoji.emojize("Starting the server..."),
        reply_markup=keyboards.host_game
    )
    out_message = send_message(
        message.chat.id,
        emoji.emojize(response),
    )

    # update tracker
    Tracker.update(state='host_game').where(Tracker.id==message.chat.id).execute()
    Game.update(message_id=out_message.message_id).where(Game.user==user).execute()


def host_leave(message, user):
    code = Game.get(Game.user==user).code
    game = Game.select().where(Game.code==code)

    for ind, row in enumerate(game):
        # update tracker
        Tracker.update(state='start').where(Tracker.id==row.user.id).execute()

        # send message to all players.
        send_message(
            row.user.id,
            emoji.emojize(":cross_mark: Game ended by Host."),
            reply_markup=keyboards.main,
        )

    # delete the game and update all players state
    Game.delete().where(Game.code==code).execute()

def host_select_roles(message, user):
    code = Game.get(Game.user==user).code
    num_players = Game.select().where(Game.code==code).count()
    send_message(message.chat.id, f"Select {num_players} roles...")
    send_message(message.chat.id, f":smiling_face_with_horns: Select Mafia Roles:", reply_markup=keyboards.mafia_roles)
    send_message(message.chat.id, f":man_police_officer_light_skin_tone: Select Citizen Roles:", reply_markup=keyboards.citizen_roles)
