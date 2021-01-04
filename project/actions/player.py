from actions import *
from actions.utils import update_users_list, generate_users_list

def player_start(message, user):
    join_code_pattern = r"^\w{4}$"
    # leave button
    if message.text == ":cross_mark: Leave":
        send_message(
            message.chat.id,
            emoji.emojize(message.text),
            reply_markup=keyboards.main,
        )

        # update tracker
        Tracker.update(state='start').where(Tracker.id==message.chat.id).execute()

        # update list of players
        # 1. get game code 2. delete player from list
        # 3. update players for everybody in the game
        game = Game.get_or_none(Game.user==user)
        if game:
            code = game.code
            Game.delete().where(Game.user==user).execute()
            update_users_list(code)

    # enter code to join a game
    elif re.match(join_code_pattern, message.text):
        count = Game.select().where(
            Game.code==message.text, Game.role=='GOD', Game.state=='start',
        ).count()
        code = message.text.upper()

        if count:
            # update game table
            Game.replace(
                id=user.id,
                user=user,
                code=code, role='player', health_status='alive',
            ).on_conflict('replace').execute()

            game = Game.select().where(
                Game.code==code, Game.state=='start',
            ).order_by(Game.role.asc())

            # send message
            response = generate_users_list(game, message.text)
            out_message = send_message(
                message.chat.id,
                emoji.emojize(response),
                reply_markup=keyboards.join_game,
            )

            # update message id and edit user messages
            Game.update(message_id=out_message.message_id).where(Game.user==user).execute()
            update_users_list(code)

        else:
            response = f":cross_mark: There are no games running with the code: {message.text}.\n\n"
            response += "Try again..."
            send_message(
                message.chat.id,
                emoji.emojize(response),
                reply_markup=keyboards.main,
            )

    else:
        send_message(
            message.chat.id,
            emoji.emojize(":cross_mark: Invalid code. Try again..."),
            reply_markup=keyboards.main,
        )


def player_leave(message, user):
    response = emoji.emojize(
        ":game_die: Join a Game\n" +
        "Ask your host for the 4-letter game code and enter it here:"
    )
    send_message(
        message.chat.id,
        response,
        reply_markup=keyboards.join_game,
    )

    # update tracker
    Tracker.update(state='join_game').where(Tracker.id==message.chat.id).execute()
