from bot import bot
import emoji
import json
from models import Tracker
from convert_numbers import english_to_persian as n2p
from finglish import f2p

DEFAULT_CHAT_ID = 73106435

def send_message(chat_id, text, reply_markup=None, emojize=True):
    """
    Send message to user.
    Returns None if user has blocked the bot.
    """
    if emojize:
        text = emoji.emojize(text)
    try:
        return bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
    except Exception as e:
        print(e)
        error_text = f"Unable to send message to {chat_id}.\n\n"
        error_text += "Message content:\n\n"
        error_text += text
        return bot.send_message(chat_id=DEFAULT_CHAT_ID, text=error_text)

def edit_message_text(text, chat_id, message_id, emojize=True):
    """
    Edit message to user.
    Returns None if user has blocked the bot.
    """
    if emojize:
        text = emoji.emojize(text)
    try:
        return bot.edit_message_text(text, chat_id=chat_id, message_id=message_id)
    except:
        error_text = f"Unable to edit message for {chat_id}.\n\n"
        error_text += "Message content:\n\n"
        error_text += text
        # bot.send_message(chat_id=DEFAULT_CHAT_ID, text=error_text)
        return

def answer_callback(text, call_id, show_alert=False):
    bot.answer_callback_query(call_id, text, show_alert=show_alert)

def edit_message_reply_markup(markup, chat_id, message_id):
    try:
        bot.edit_message_reply_markup(
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=markup,
        )
    except:
        print('reply markup is not modified!')

def next_n(iterator, N):
    """
    Returns N elements of an iterator each time.
    """
    try:
        items = []
        for _ in range(N):
            items.append(next(iterator))
        return items
    except StopIteration:
        if items:
            return items
        return None

def update_state(user, state):
    Tracker.update(state=state).where(Tracker.id==user.id).execute()
