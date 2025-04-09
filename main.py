import datetime
import os

import discord
from discord.ext import commands

TOKEN = os.environ["DISCORD_API_KEY"] # APIキー

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")

@bot.event
async def on_ready():
    pass

@bot.command()
async def get(ctx):
    info = get_menu_info() # メニュー表取得
    today = str(datetime.datetime.now().day)
    for i in info:
        if today in i[0][1:]:
            idx = 1
            while True:
                if today in i[0][idx]:
                    break
                idx += 1
            msg = f"今日の日替わりメニュー\n"
            for m in i[1:]:
                msg += f"{m[0]}: {m[idx]}\n"
            break
    await ctx.send(msg)

def main():
    bot.run(TOKEN)

if __name__ == "__main__":
    main()