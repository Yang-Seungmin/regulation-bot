import discord

from bot.regulationbot import bot
from bot.secrets import regulation_bot_key

if __name__ == '__main__':
    bot.run(regulation_bot_key)