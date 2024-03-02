import os 
import discord 

from dotnev import load_dotnev

load_dotenv()
TOKEN = os.getenv("MTIxMzUzNzI3MzgxMTgzMjg0Mg.GSpTc2.LXNRPADODbVG91NWnL1SjsFf-oQePCcUbFLqFU")

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)