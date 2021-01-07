from utils import answer_callback
from models import RoleSelectionTracker, Role, Tracker
from actions.host import create_role_selection_menu
from utils import edit_message_reply_markup
from actions.host import send_current_roles, get_players

def respond_role_menu(call, user):
    role = Role.get(Role.role_name == call.data)
    prev_value = RoleSelectionTracker.get(
        RoleSelectionTracker.user==user, RoleSelectionTracker.role == role
    ).checked

    new_value = not prev_value
    RoleSelectionTracker.update(checked=new_value).where(
        RoleSelectionTracker.user==user, RoleSelectionTracker.role == role
    ).execute()

    if new_value:
        answer_callback(f"نقش {role.role_name} اضافه شد.", call.id)
    else:
        answer_callback(f"نقش {role.role_name} حذف شد.", call.id)

    # update role team keyboard
    if role.team == "مافیا":
        message_id = Tracker.get(Tracker.id==user.id).mafia_message_id
    else:
        message_id = Tracker.get(Tracker.id==user.id).citizen_message_id

    # edit reply keyboard with new values
    edit_message_reply_markup(
        create_role_selection_menu(user, role.team),
        chat_id=user.id,
        message_id=message_id,
    )

    # send the new list of roles to every player
    players = get_players(user, include_god=True)
    num_players = len(players) - 1
    for player in players:
        send_current_roles(player, num_players, edit=True)
