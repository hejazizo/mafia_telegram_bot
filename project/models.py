from peewee import *
import datetime
import os

db = MySQLDatabase(
    'mafiabot',
    user='mafiabot',
    password="R$7ZLFb{O}AvK_o&Rjq|",
    host='localhost',
    port=3306
)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField()
    username = TextField()

class Tracker(BaseModel):
    id = IntegerField(primary_key=True)
    state = TextField(default='start')

class Game(BaseModel):
    id = IntegerField(primary_key=True)
    user = ForeignKeyField(model=User)

    code = TextField()

    role = TextField()
    mafia_role = TextField()
    health_status = TextField(default="Alive")
    message_id = IntegerField()

    state = TextField(default="start")

class GameSettings(BaseModel):
    """
    Specific settings for each user (host).
    """
    user = ForeignKeyField(model=User)
    message_id = IntegerField()
    inheritance = BooleanField(default=True)
    # ---------------------------
    # mafia
    # ---------------------------
    # shadow mafia number of push
    shadow_mafia_num_push = IntegerField(default=2)
    shadow_mafia_knows_mafia = BooleanField(default=True)

    # insane mafia
    # nothing to add

    # gangster mafia
    gangster_mafia_num_guns = IntegerField(default=1)

    # boss
    # nothing to add

    # negotiator mafia
    negotiator_mafia_num_dead_mafia = IntegerField(default=2)

    # terrorist
    # nothing to add

    # witch
    # nothing to add

    # ---------------------------
    # citizen
    # ---------------------------
    # simple citizen
    # nothing to add

    # loyal citizen
    # nothing to add

    # doctor
    doctor_heal_num_1 = IntegerField(default=3)
    doctor_heal_num_2 = IntegerField(default=3)
    doctor_heal_num_3 = IntegerField(default=2)
    doctor_heal_num_4 = IntegerField(default=2)
    doctor_heal_num_5 = IntegerField(default=1)

    # nurse
    # nothing to add

    # cowboy
    # nothing to add

    # snowman
    snowman_num_shot = IntegerField(default=3)

    # sniper
    # nothing to add

    # priest
    # nothing to add

    # gunman
    gunman_num_real_guns = IntegerField(default=2)
    gunman_num_fake_guns = IntegerField(default=2)
    gunman_self_give = BooleanField(default=True)
    gunman_real_self_give = BooleanField(default=False)
    gunman_max_gun_per_day = IntegerField(default=1)

    # armored
    # nothing to add

    # reporter
    # nothing to add

    # interrogator
    # nothing to add

    # detective
    # nothign to add

    # jesus
    jesus_self_heal = BooleanField(default=True)
    jesus_max_nights_passed = IntegerField(default=2)
    jesus_heal_deadline_after_death = IntegerField(default=2)

    # postman
    # nothing to add

    # lover
    # nothing to add

class GameSettingsKeys(BaseModel):
    callback_data = TextField()
    text = TextField()
    max_value = IntegerField()
    is_boolean = BooleanField()

    # row and column specify the keys layout
    row = IntegerField()
    column = IntegerField()

class Poll(BaseModel):
    poll_id = BigIntegerField()
    user = ForeignKeyField(model=User)
    option_id = IntegerField()
    option = TextField()
    checked = BooleanField(default=False)

class Role(BaseModel):
    recorder = ForeignKeyField(model=User)
    default_role = BooleanField(default=False)
    role = TextField()
    team = TextField(default='citizen')
    description = TextField()
