import random

import discord
import asyncio

import discord
from discord import Message
from discord.ext import commands

from bot.emoticons.gyumoticons import gyumoticons, gyupostfixes, send_regulation_postfix_emoji
from bot.gyutactoe import *
from bot.messages.gyucommands import help_commands
from bot.messages.gyuerrors import send_regulation_unknown_error_message, handle_unknown_exception
from bot.messages.gyumessages import send_regulation_dorai_message
from bot.options import *
from bot.regulation_secrets import opt_regulation_init_message_channel_id, opt_regulation_message_gtt_channel_id, \
    opt_regulation_message_test_channel_id
from bot.source.gyutactoedb import get_gtt_win_count, get_gtt_lose_count, get_gtt_draw_count
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
    if ctx.channel.id not in [opt_regulation_message_gtt_channel_id, opt_regulation_message_test_channel_id]:
        await ctx.send('저쪽가서해')
        await ctx.send('미친사람들아')
        await send_regulation_postfix_emoji(ctx)
        return

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
                    await ctx.send('{} 님이 이김'.format(winner.mention))
                    await ctx.send('ㄹㅈㄷ')
                else:
                    await ctx.send('미친 사람들인가')
                    await ctx.send('ㄹㅈㄷ')
                await send_regulation_postfix_emoji(ctx)
                gyutactoe_game = GyuTacToe()
            return

        if type == '전적':
            win = get_gtt_win_count(ctx.author)
            lose = get_gtt_lose_count(ctx.author)
            draw = get_gtt_draw_count(ctx.author)

            if win + lose + draw == 0:
                await ctx.send("님 규택토 한판 하고 와요")
                await ctx.send("인싸잖ㅇ..")
                await send_regulation_postfix_emoji(ctx)
                return

            embed = discord.Embed(
                title="{0}의 규택토 전적".format(ctx.author.name),
                description="혼자서 한 게임은 버그라 안넣음",
                colour=discord.Colour.red() if win < lose else discord.Colour.green()
            )
            embed.add_field(name="승리", value=f"{win}게임", inline=True)
            embed.add_field(name="패배", value=f"{lose}게임", inline=True)
            embed.add_field(name="무승부", value=f"{draw}게임", inline=True)
            embed.add_field(name="승률", value="{:0.1f}%".format(win / (win + lose + draw) * 100), inline=False)
            await ctx.send(embed=embed)
            return

        if type in help_commands:
            await ctx.send(
                '''규택토 사용법
```
!규택토 : 현재 규택토 상태 표시
!규택토 참여 : 규택토 참여하기
!규택토 위치 [1~3] [1~3]: 해당 위치에 표시하기
!규택토 전적 : 자신의 전적 보기
!규택토 위치 1 1 은 왼쪽 위, !규택토 위치 3 3은 오른쪽 아래에 표시
```'''
            )
            await send_regulation_postfix_emoji(ctx)
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
        await ctx.send('거기 {} 님이 먹음'.format(e.user.mention))
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

@bot.command(name="삭제")
async def delete_user_messages(ctx, message=""):  # 메세지 단일 또는 다중 삭제

    user = message.author
    che = False
    msg = message.message.content[4:]

    async def delete_message(num, info_user):  # num 갯수의 메세지 삭제 다 삭제 후 return True

        counter = 0

        # 메세지의 user가 명령어 호출한 유저와 같은지 확인
        if msg.author != info_user:
            return False

        # 가져올 메세지의 조건
        def predicate(message):
            return not message.author.bot  # not bot message

        #최근 500개의 메세지 중 삭제
        async for msg in ctx.history(limit=500).filter(predicate):

            # 메세지의 user가 명령어 호출한 유저와 같은지 확인
            if msg.author == info_user:
                await msg.delete(delay=0)
                await asyncio.sleep(0.1)
                counter += 1

            # 정해진 갯수의 메세지 삭제 후
            if counter == num:
                return True

    # msg 비어있을 시
    if msg == '':
        s_msg = await ctx.send(embed=discord.Embed(title=None, description="얼마나 메세지 'regulation' 해야하는거임!", colour=0x7289da))
        await s_msg.delete(delay=3)

    # msg에 숫자값이 입력됬을경우
    elif int(msg) > 0:

        s_msg = await ctx.send(embed=discord.Embed(title=None, description=
        "3초안에 형들 " + str(msg) + "개 채팅 다 먹어버릴거야 ㅇㅅㅇ)/", colour=0x7289da))

        await s_msg.delete(delay=3)
        # await asyncio.sleep(3)
        che = await delete_message(int(msg), user)

        if che == True:
            # await asyncio.sleep(int(msg) / 5)
            s_msg = await ctx.send(embed=discord.Embed(title=None, description=
            "맛도리군요 ㅇㅅㅇ)b", colour=0x7289da))
            await s_msg.delete(delay=3)

    # 양수 이외 값 입력시
    else:
        s_msg = await ctx.send(embed=discord.Embed(title=None, description="꺨깔꼴... 다시 입..려..", colour=0x7289da))
        await s_msg.delete(delay=3)