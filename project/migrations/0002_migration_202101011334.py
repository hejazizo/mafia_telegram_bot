# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class Game(peewee.Model):
    code = TextField()
    username = IntegerField(unique=True)
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


def forward(old_orm, new_orm):
    old_game = old_orm['game']
    game = new_orm['game']
    return [
        # Convert datatype of the field game.username: TEXT -> INT
        game.update({game.username: old_game.username.cast('SIGNED')}).where(old_game.username.is_null(False)),
    ]


def backward(old_orm, new_orm):
    old_game = old_orm['game']
    game = new_orm['game']
    return [
        # Don't know how to do the conversion correctly, use the naive
        game.update({game.username: old_game.username}).where(old_game.username.is_null(False)),
    ]
