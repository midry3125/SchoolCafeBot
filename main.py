import datetime
import ctypes
import json
import os
import sys

import discord
from discord.ext import commands, tasks

intents = discord.Intents.all()
intents.message_content = True
intents.reactions = True
bot = commands.Bot(intents=intents, command_prefix="!")
now = datetime.datetime.now()

get_info = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(sys.argv[0]), "GetInfo.so")).get_info
get_info.restype = ctypes.c_char_p

def update_date():
    global now
    now = datetime.datetime.now()

@tasks.loop(seconds=60)
async def schedule():
    await bot.wait_until_ready()
    if datetime.datetime.now().day != now.day:
        update_date()
        msg = make_today_message()
        chan = bot.get_channel(CHANNEL)
        await chan.send(msg)

@bot.event
async def on_ready():
    pass

@bot.command()
async def today(ctx):
    update_date()
    msg = make_today_message()
    await ctx.send(msg)

@bot.command()
async def tomorrow(ctx):
    update_date()
    t = now + datetime.timedelta(days = 1)
    msg = make_message(t.day)
    await ctx.send(msg)

@bot.command()
async def week(ctx):
    update_date()
    msg = make_week_message()
    await ctx.send(msg)

@bot.command()
async def day(ctx, d: int):
    update_date()
    msg = make_message(d)
    await ctx.send(msg)

def make_today_message():
    return make_message()

def make_week_message():
    return make_message(week=True)

def make_message(day=now.day, week=False):
    info = json.loads(get_info())
    day = str(day)
    for i in info:
        for n, d in enumerate(i[0][1:]):
            if day == d.split("日")[0].strip():
                idx = n + 1
                break
        else:
            continue
        if week:
            msg = ""
            for n in range(1, len(i)):
                msg += f"{i[0][n]}のメニュー\n"
                for m in range(1, len(i[0])):
                    msg += "{}: {}\n".format(i[m][0], i[m][n].replace("\n", ", "))
                msg += "\n"
            return msg
                
        else:
            msg = "{}の日替わりメニュー\n".format("今日" if day == today else f"{day}日")
            for m in i[1:]:
                msg += "{}: {}\n".format(m[0], m[idx].replace("\n", ", "))
            return msg
    return "情報がありません"

def main():
    global CHANNEL
    TOKEN = os.environ["DISCORD_API_KEY"] # APIキー
    CHANNEL = os.environ["DISCORD_CHANNEL_ID"]
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
