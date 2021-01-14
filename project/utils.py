from bot import bot
import emoji
import json
from models import Tracker
from convert_numbers import english_to_persian as n2p
from finglish import f2p
import logging
import argparse

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

def configure_colored_logging(loglevel):
    import coloredlogs

    field_styles = coloredlogs.DEFAULT_FIELD_STYLES.copy()
    field_styles["asctime"] = {}
    level_styles = coloredlogs.DEFAULT_LEVEL_STYLES.copy()
    level_styles["debug"] = {}
    coloredlogs.install(
        level=loglevel,
        use_chroot=False,
        fmt="%(asctime)s %(levelname)-8s %(name)s  - %(message)s",
        level_styles=level_styles,
        field_styles=field_styles,
    )

def add_logging_options(parser):
    """Add options to an argument parser to configure logging levels."""

    logging_arguments = parser.add_argument_group("Python Logging Options")

    # arguments for logging configuration
    logging_arguments.add_argument(
        "-v",
        "--verbose",
        help="Be verbose. Sets logging level to INFO.",
        action="store_const",
        dest="loglevel",
        const=logging.INFO,
    )
    logging_arguments.add_argument(
        "-vv",
        "--debug",
        help="Print lots of debugging statements. Sets logging level to DEBUG.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    logging_arguments.add_argument(
        "--quiet",
        help="Be quiet! Sets logging level to WARNING.",
        action="store_const",
        dest="loglevel",
        const=logging.WARNING,
    )

def create_argument_parser() -> argparse.ArgumentParser:
    """Parse all the command line arguments for the training script."""

    parser = argparse.ArgumentParser(
        prog="mafiabot",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Mafia Telegram Bot command line interface.",
    )

    # parser.add_argument(
    #     "--argument",
    #     action="store_true",
    #     default=,
    #     help="",
    # )

    add_logging_options(parser)

    return parser