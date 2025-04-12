import datetime
import json
import os
import sys

import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")

@bot.event
async def on_ready():
    pass

@bot.command()
async def today(ctx):
    msg = make_today_message()
    await ctx.send(msg)

@bot.command()
async def week(ctx):
    msg = make_week_message()
    await ctx.send(msg)

@bot.command()
async def day(ctx, d):
    msg = make_message(d)
    await ctx.send(msg)

def make_today_message():
    return make_message()

def make_week_meaage():
    return make_message(week=True)

def make_message(day=None, week=False):
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        info = json.load(f)
    if day is None:
        day = str(datetime.datetime.now().day)
    for i in info:
        for n, d in enumerate(i[0][1:]):
            if day == d.split("日")[0].strip():
                idx = n + 1
                break
        else:
            continue
        if week:
            msg = ""
            for n in range(len(i)-1):
                msg += f"{i[0][n+1]}のメニュー\n"
                for m in range(len(i[0])-1):
                    msg += "{}: {}\n".format(i[m+1][0], i[m+1][n+1].replace("\n", ", "))
                msg += "\n"
            return msg
                
        else:
            msg = f"今日の日替わりメニュー\n"
            for m in i[1:]:
                msg += "{}: {}\n".format(m[0], m[idx].replace("\n", ", "))
            return msg
    return "情報がありません"

def main():
    TOKEN = os.environ["DISCORD_API_KEY"] # APIキー
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
