import json
from data import DATA_PATH
from pathlib import Path

BOT_ID = 73106435
ROLES = json.load(open(Path(DATA_PATH, "roles.json")))
DEFAULT_LOG_LEVEL = "INFO"
BOT_INTERVAL = 0.1
BOT_TIMEOUT = 120