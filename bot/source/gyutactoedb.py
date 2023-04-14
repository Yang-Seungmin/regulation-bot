from discord import User
from peewee import *

from bot.source.database import db


class GyutactoeResult(Model):
    datetime = DateTimeField()
    player1 = TextField()
    player2 = TextField()
    winner = CharField()
    record = TextField()

    class Meta:
        database = db


def get_gtt_win_count(user: User):
    return GyutactoeResult.select().where(GyutactoeResult.player1 == user.id, GyutactoeResult.winner == '1').count() + \
        GyutactoeResult.select().where(GyutactoeResult.player2 == user.id, GyutactoeResult.winner == '2').count()


def get_gtt_lose_count(user: User):
    return GyutactoeResult.select().where(GyutactoeResult.player2 == user.id, GyutactoeResult.winner == '1').count() + \
        GyutactoeResult.select().where(GyutactoeResult.player1 == user.id, GyutactoeResult.winner == '2').count()


def get_gtt_draw_count(user: User):
    return GyutactoeResult.select().where(GyutactoeResult.player1 == user.id, GyutactoeResult.winner == 'N').count() + \
        GyutactoeResult.select().where(GyutactoeResult.player2 == user.id, GyutactoeResult.winner == 'N').count()