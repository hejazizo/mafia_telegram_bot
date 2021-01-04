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

class Poll(BaseModel):
    poll_id = BigIntegerField()
    user = ForeignKeyField(model=User)
    option_id = IntegerField()
    option = TextField()
    checked = BooleanField(default=False)
