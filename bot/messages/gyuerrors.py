import random
import traceback

from discord import Message
from discord.ext.commands import Bot

from bot.emoticons.gyumoticons import send_regulation_postfix_emoji
from bot.regulation_secrets import opt_regulation_message_test_channel_id


async def handle_unknown_exception(bot: Bot, ctx: Message):
    await bot.get_channel(opt_regulation_message_test_channel_id)\
        .send(f'작성자: {ctx.author}\n내용: {ctx.content}```\n{traceback.format_exc()}\n```')
    await send_regulation_unknown_error_message(ctx)


async def send_regulation_unknown_error_message(ctx: Message):
    await ctx.send('아니 형 이거 버그임')
    await send_regulation_postfix_emoji(ctx)
