from bot import bot
import emoji
import json

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
    except:
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