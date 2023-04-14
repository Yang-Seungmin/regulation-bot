import random

gyumoticons = (":fastregulation:", ":mayakregulation:", ":shakeregulation:")
gyupostfixes = ['ㅇㅁㅇ);>', '._.)>', 'ㅇㅅㅇ)=3', 't(._.t', 'ㅇㅅㅇ)']


async def send_regulation_postfix_emoji(ctx):
    await ctx.send(random.choice(gyupostfixes))
