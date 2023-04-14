import discord

from bot.regulationbot import bot
from bot.regulation_secrets import regulation_bot_key
from bot.source.database import db
from bot.source.gyutactoedb import GyutactoeResult

if __name__ == '__main__':
    db.connect()

    if not GyutactoeResult.table_exists():
        GyutactoeResult.create_table()

    bot.run(regulation_bot_key)
