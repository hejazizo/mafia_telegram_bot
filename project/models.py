from peewee import *
import datetime
import os

db = MySQLDatabase(
    'mafiabot',
    user='mafiabot',
    password=os.getenv("mafiabotdb_password"),
    host='localhost',
    port=3306
)

class BaseModel(Model):
    class Meta:
        database = db


class Tracker(BaseModel):
    username = IntegerField(unique=True)
    state = TextField(default='start')


class Game(BaseModel):
    code = TextField()
    username = IntegerField(unique=True)
    role = TextField()
    health_status = TextField(default="Alive")
    message_id = IntegerField()