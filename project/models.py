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


class Tracker(BaseModel):
    username = IntegerField(primary_key=True)
    state = TextField(default='start')


class Game(BaseModel):
    username = IntegerField(primary_key=True)
    code = TextField()

    role = TextField()
    health_status = TextField(default="Alive")
    message_id = IntegerField()
