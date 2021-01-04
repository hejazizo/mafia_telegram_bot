from telebot import types
import emoji


def create_keyboard(keys, row_width=2, use_aliases=True):
    """
    Creates python reply keyboards.
    """
    markup = types.ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=True)
    for ind in range(0, len(keys), row_width):
        start = ind
        end = start+row_width
        if ind+row_width >= len(keys):
            end = len(keys)

        # add keys to keyboards
        markup.add(*[
            types.KeyboardButton(
                emoji.emojize(key, use_aliases=True)
            ) for key in keys[start:end]]
        )
    return markup

def create_inline_keyboard(json_string):
    markup = types.InlineKeyboardMarkup.de_json(json_string)
    return markup

class Keyboards:
    def __init__(self):
        self.main = create_keyboard(
            keys=[":desktop_computer: Host a Game", ":game_die: Join a Game"]
        )
        self.join_game = create_keyboard(
            keys=[':cross_mark: Leave']
        )
        self.host_game = create_keyboard(
            keys=[':arrow_right: Next', ':x: Leave']
        )

        self.send_roles = create_keyboard(
            keys=[":email: Send roles", ":cross_mark: Leave",]
        )

# ------------------------------------
# Loading keyboards
# ------------------------------------
keyboards = Keyboards()