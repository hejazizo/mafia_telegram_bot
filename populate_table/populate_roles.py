import sys
from pathlib import Path

project_path = str(Path(__file__).resolve().parent.parent.absolute())
sys.path.append(project_path)

import json

from project.models import Role, User
from collections import defaultdict

user = User.get(User.username=='Aliii_H93')

roles = open('roles.txt')

roles_desc = defaultdict(str)
desc = ""
role = None
for ind, line in enumerate(roles):
    if ind == 0:
        mafia_roles = [item.strip() for item in line.strip().split(" - ")]
        continue
    if ind == 1:
        citizen_roles = [item.strip() for item in line.strip().split(" - ")]
        continue

    if line.strip() in mafia_roles:
        if desc:
            Role.insert(
                recorder=user,
                locked = True,
                role = role,
                team='مافیا',
                callback_data=role,
                description=desc,
            ).execute()
            desc = ""
        role = line.strip()
    elif line.strip() in citizen_roles:
        if desc:
            Role.insert(
                recorder=user,
                locked = True,
                role = role,
                team='شهروند',
                callback_data=role,
                description=desc,
            ).execute()
            desc = ""
        role = line.strip()
    else:
        desc += line

if desc:
    Role.insert(
        recorder=user,
        locked = True,
        role = role,
        team='شهروند',
        callback_data=role,
        description=desc,
    ).execute()
    desc = ""