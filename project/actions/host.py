from actions import *
from actions.utils import generate_users_list
from constants import ROLES
from utils import next_n
from models import Role


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
    update_state(user, 'host_game')
    Game.update(message_id=out_message.message_id).where(Game.user==user).execute()


def host_leave(message, user):
    code = Game.get(Game.user==user).code
    game = Game.select().where(Game.code==code)

    for row in game:
        # update tracker
        update_state(row.user, 'start')

        # send message to all players.
        send_message(
            row.user.id,
            emoji.emojize(":cross_mark: Game ended by Host."),
            reply_markup=keyboards.main,
        )

    # delete the game and update all players state
    Game.delete().where(Game.code==code).execute()
    Poll.delete().where(Poll.user==user).execute()

def host_select_roles_with_poll(message, user):
    players = get_players(user, include_god=True)
    num_players = len(players) - 1
    send_message(
        message.chat.id, f":high_voltage: You have to select {num_players} roles now...",
        reply_markup=keyboards.send_roles
    )

    send_poll(message.chat.id, "mafia")
    send_poll(message.chat.id, "citizen")

    poll = Poll.select().where(Poll.user==user, Poll.checked==True)
    for player in players:
        send_current_roles(player.user, poll, num_players)
    # send_message(message.chat.id, f":smiling_face_with_horns: Select Mafia Roles:", reply_markup=keyboards.mafia_roles)
    # send_message(message.chat.id, f":man_police_officer_light_skin_tone: Select Citizen Roles:", reply_markup=keyboards.citizen_roles)

def host_select_roles(message, user):
    pass

def host_send_roles(message, user):
    players = get_players(user)
    roles = get_selected_roles(user)

    if len(players) > len(roles):
        send_message(user.id, ":cross_mark: " f"تعداد بازیکن‌ها بیشتر از نقش‌هاست.")
        return
    if len(players) < len(roles):
        send_message(user.id, ":cross_mark: " f"تعداد بازیکن‌ها کمتر از نقش‌هاست.")
        return

    # shuffle players and send their roles.
    players_id = [player.user.id for player in players]
    random.shuffle(roles)

    for role, player_id in zip(roles, players_id):
        role_db = Role.get(Role.role == role)
        text = f":bust_in_silhouette: نقش شما: <b>{role}</b>\n"
        text += f":high_voltage: تیم: <b>{role_db.team}</b>\n\n"
        text += ":page_facing_up: <b>شرح نقش:</b>\n"
        text += role_db.description
        send_message(player_id, text)
        Game.update(mafia_role=role).where(Game.id==player_id).execute()

    # get updated players (mafia_role is updated now)
    players = get_players(user)
    send_message(user.id, get_players_roles(players))

def send_current_roles(user, poll, num_players, edit=False):

    text = ":busts_in_silhouette: نقش‌های انتخاب شده:\n\n"
    for ind, row in enumerate(poll):
        text += f"{n2p(ind+1)}. {row.option}\n"

    text += "\n\n"
    if len(poll) > num_players:
        text += ":warning_selector: <b>"
        text += f"{n2p(len(poll)-num_players)} "
        text += "نقش را حذف کنید.\n"
        text += " ("
        text += f"تعداد بازیکن‌ها: {num_players} | "
        text += f"تعداد نقش‌ها: {len(poll)}"
        text += ")"
        text += "</b>"
    elif len(poll) < num_players:
        text += ":warning_selector: <b>"
        text += f"{n2p(num_players-len(poll))} "
        text += "نقش دیگر انتخاب کنید.\n"
        text += " ("
        text += f"تعداد بازیکن‌ها: {num_players} - "
        text += f"تعداد نقش‌ها: {len(poll)}"
        text += ")"
        text += "</b>"
    else:
        text += ":white_heavy_check_mark: <b>"
        text += "تعداد نقش‌ها و بازیکن‌ها مساوی است."
        text += "</b>"

    if edit:
        message_id = Game.get(Game.user==user).message_id
        edit_message_text(text, user.id, message_id)
        return

    out_message = send_message(user.id, text)
    Game.update(message_id=out_message.message_id).where(Game.user==user).execute()


def send_poll(chat_id, role_type):
    roles = iter(ROLES[role_type])
    batch = next_n(roles, 10)
    while batch:
        options = list(batch)
        out_message = bot.send_poll(
            chat_id, question=f"Select {role_type.upper()} Roles:",
            options=batch,
            is_anonymous=False,
            allows_multiple_answers=True,
        )
        batch = next_n(roles, 10)

        # write in database
        user = User.get(id=chat_id)
        for option_id, option in enumerate(options):
            Poll.replace(
                poll_id=out_message.poll.id,
                user=user,
                option_id=option_id,
                option=option,
            ).on_conflict_replace().execute()


def host_roles_poll(poll):
    if poll.options_ids:
        Poll.update(checked=True).where(
            Poll.poll_id==poll.poll_id,
            Poll.option_id.in_(poll.options_ids)
        ).execute()
    else:
        Poll.update(checked=False).where(
            Poll.poll_id==poll.poll_id,
        ).execute()

    user=User.get(id=poll.user.id)
    players = get_players(user, include_god=True)
    num_players = len(players) - 1

    # retrieve data from poll db
    poll = Poll.select().where(Poll.user==user, Poll.checked==True)
    for player in players:
        send_current_roles(player.user, poll, num_players, edit=True)


def get_players(user, include_god=False):
    game_code = Game.get(Game.user==user).code
    if include_god:
        return Game.select().where(Game.code==game_code)

    return Game.select().where(Game.code==game_code, Game.role != "GOD")

def get_selected_roles(user):
    poll = Poll.select().where(Poll.user==user, Poll.checked==True)
    return [row.option for row in poll]

def get_players_roles(players):
    text = ":busts_in_silhouette: فهرست نقش‌ها:\n\n"
    for ind, player in enumerate(players):
        text += f"{n2p(ind+1)}. "

        text += f"{f2p(player.user.name)} (@{player.user.username}): <b>{player.mafia_role}"
        text += "</b>"
        text += "\n"

    return text