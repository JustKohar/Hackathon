# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("MTIxMzUzNzI3MzgxMTgzMjg0Mg.GSpTc2.LXNRPADODbVG91NWnL1SjsFf-oQePCcUbFLqFU")
GUILD = os.getenv('1213537641597894748')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

client.run(TOKEN)