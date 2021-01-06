import sys
from pathlib import Path

project_path = str(Path(__file__).resolve().parent.parent.absolute())
sys.path.append(project_path)

import json

from project.models import GameSettingsKeys

keys_file = json.loads(open("settings.json").read())

for row, keys in enumerate(keys_file["inline_keyboard"]):
    for column, key in enumerate(keys):
        key['is_boolean'] = key["max_value"] == 1
        key['row'] = row
        key['column'] = column
        GameSettingsKeys.insert(**key).execute()

# -------------------------------------------------
json_data = {
    "inline_keyboard": []
}
game_settings_keys = GameSettingsKeys.select().order_by(['row, column'])

for key in game_settings_keys:
    data = key.__dict__["__data__"]
    data["is_boolean"] = int(data["is_boolean"])
    if key.column == 0:
        json_data["inline_keyboard"].append([data])
        continue

    json_data["inline_keyboard"][-1].append(data)

from pprint import pprint
json_data = str(json_data).replace("'", '"')
json.loads(json_data)