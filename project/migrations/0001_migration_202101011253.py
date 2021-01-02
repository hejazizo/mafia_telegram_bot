# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Game(peewee.Model):
    code = TextField()
    username = TextField(unique=True)
    role = TextField()
    health_status = TextField(default='Alive')
    message_id = IntegerField()
    class Meta:
        table_name = "game"


@snapshot.append
class Tracker(peewee.Model):
    username = IntegerField(unique=True)
    state = TextField(default='start')
    class Meta:
        table_name = "tracker"


