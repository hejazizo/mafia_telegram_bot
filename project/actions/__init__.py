import random
import re
import string
from pathlib import Path

import emoji
from bot import bot
from constants import BOT_ID
from keyboards import (create_inline_keyboard,
                       create_inline_keyboard_from_json_string,
                       create_keyboard, keyboards)
from models import Game, GameSettings, Poll, Tracker, User, db, RoleSelectionTracker

from utils import edit_message_text, f2p, n2p, send_message, update_state

ACTIONS_PATH = Path(__file__).parent
