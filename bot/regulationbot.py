import random

import discord

import discord
from discord import Message
from discord.ext import commands

from bot.emoticons.gyumoticons import gyumoticons, gyupostfixes, send_regulation_postfix_emoji
from bot.gyutactoe import *
from bot.messages.gyuerrors import send_regulation_unknown_error_message, handle_unknown_exception
from bot.messages.gyumessages import send_regulation_dorai_message
from bot.options import *
from bot.regulation_secrets import opt_regulation_init_message_channel_id
from bot.utils import to_upper

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

gyutactoe_game: GyuTacToe = GyuTacToe()


@bot.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    print("Channels: ")
    for channel in bot.get_all_channels():
        print(" - {0}: {1}".format(channel.id, channel.name))

    await bot.get_channel(1094921384456630354).send(content="부")
    await bot.get_channel(1094921384456630354).send(content="활")
    if opt_regulation_send_init_message:
        await bot.get_channel(opt_regulation_init_message_channel_id).send(content="부")
        await bot.get_channel(opt_regulation_init_message_channel_id).send(content="활")


@bot.event
async def on_message(ctx):
    if random.random() < opt_regulation_question_sign_frequency and ctx.author.id != bot.user.id:
        await ctx.channel.send('?')

    await bot.process_commands(ctx)


@bot.command(name="규모지")
async def ping(ctx):
    regulation_emoji = ['<:{name}:{id}>'.format(name=e.name, id=e.id) for e in ctx.guild.emojis if
                        'regulation' in e.name]
    await ctx.send(' '.join(regulation_emoji))


@bot.command(name="규타일")
async def gyu_tile(ctx, type: str = '랜덤', x: int = 5, y: int = 5):
    try:
        if type != '랜덤':
            await send_regulation_unknown_error_message()
        regulation_emoji = ['<:{name}:{id}>'.format(name=e.name, id=e.id) for e in ctx.guild.emojis if
                            'regulation' in e.name]
        get_regulation = lambda _x, _y: random.choice(regulation_emoji)

        result = [[get_regulation(_x, _y) for _x in range(0, x)] for _y in range(0, y)]

        await ctx.send('\n'.join(map(lambda row: ' '.join(row), result)))
    except discord.errors.HTTPException as e:
        if e.status == 400:
            await send_regulation_dorai_message(ctx)
        else:
            await handle_unknown_exception(bot, ctx)
    except:
        await handle_unknown_exception(bot, ctx)


@bot.command(name="규며듦점수")
async def gyu_score(ctx):
    embed = discord.Embed(title="규며듦 점수", description=None)
    embed.add_field(name="{0}의 규며듦 점수".format(ctx.author.name), value="0점")
    embed.set_footer(text="개발중...")
    await ctx.send(embed=embed)


@bot.command(name="규택토")
async def gyu_gyutactoe(ctx, type="", x: int = -1, y: int = -1):
    global gyutactoe_game
    gyutactoe_game.transparent = [e for e in ctx.guild.emojis if 'transparent' in e.name][0]
    regulation_emoji = [e for e in ctx.guild.emojis if
                        'regulation' in e.name]

    try:
        if type == "참여":
            enter_emoji = random.choice([emoji for emoji in regulation_emoji if emoji not in gyutactoe_game.emojies])
            if not gyutactoe_game.enter(ctx.author, enter_emoji):
                await ctx.send('{user} <:{name}:{id}>'.format(user=ctx.author.mention, name=enter_emoji.name, id=enter_emoji.id))
                await ctx.send('사람 더 모이면 할거임 ㅅㄱㅂ')
            else:
                await ctx.send('{user} <:{name}:{id}>'.format(user=ctx.author.mention, name=enter_emoji.name, id=enter_emoji.id))
                await ctx.send('굿')

            return

        if type == "위치":
            tile, winner, is_end = gyutactoe_game.go(ctx.author, x, y)
            await ctx.send(tile)

            if is_end:
                if winner is not None:
                    await ctx.send('{} 이(가) 이김'.format(winner.mention))
                    await ctx.send('ㄹㅈㄷ')
                else:
                    await ctx.send('미친 사람들인가')
                    await ctx.send('ㄹㅈㄷ')
                await send_regulation_postfix_emoji(ctx)
                gyutactoe_game = GyuTacToe()
            return

        if len(gyutactoe_game.players) == 0:
            await ctx.send('규택토 해버려?')
            await ctx.send('팍씨')
            return

        if not gyutactoe_game.is_all_user_entered():
            await ctx.send('사람 더 모이면 할거임 ㅅㄱㅂ')
            return

        if gyutactoe_game.is_all_user_entered() and not gyutactoe_game.is_end():
            await ctx.send('전')
            await ctx.send('규택토 하는 중임다')
            await send_regulation_postfix_emoji(ctx)
            await ctx.send(gyutactoe_game.get_gyutactoe_tile())
            return

        await send_regulation_unknown_error_message(ctx)
    except TurnError as e:
        await ctx.send('님 머함')
        await send_regulation_postfix_emoji(ctx)
        await ctx.send('{} 형 해요'.format(e.real_turn.mention))
    except PositionIsDuplicatedMeError as e:
        await ctx.send('님 머함')
        await ctx.send('거기 님이 먹음')
        await send_regulation_postfix_emoji(ctx)
    except PositionIsDuplicatedOtherError as e:
        await ctx.send('님 머함')
        await ctx.send('거기 {} 이(가)이 먹음'.format(e.user.mention))
        await send_regulation_postfix_emoji(ctx)
    except UserIsNotFullError as e:
        await ctx.send('사람 더 모이면 할거임 ㅅㄱㅂ')
    except UserIsFullError as e:
        await ctx.send('전')
        await ctx.send('규택토 하는 중임다')
        await send_regulation_postfix_emoji(ctx)
    except IndexError:
        await ctx.send('님 머함')
        await ctx.send('버그 ㄴ')
        await send_regulation_postfix_emoji(ctx)
    except Exception as e:
        await handle_unknown_exception(bot, ctx)


@bot.command(name="허허")
async def gyu_gjgj(ctx):
    await ctx.send('재재')


@bot.command(name="재재")
async def gyu_jaejae(ctx):
    await ctx.send('원원')


@bot.command(name="원원")
async def gyu_wonwon(ctx):
    await ctx.send('승승')


@bot.command(name="승승")
async def gyu_seungseung(ctx):
    await ctx.send('주주')


@bot.command(name="주주")
async def gyu_seungseung(ctx):
    await ctx.send('young')


@bot.command(name="주")
async def gyu_seungseung(ctx):
    await ctx.send('Young')


@bot.command(name="스스")
async def gyu_seuseu(ctx):
    await ctx.send('몰킴')
