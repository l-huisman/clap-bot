import os
import discord

from dotenv import load_dotenv
from clappy_boy import ClappyBoy

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
channel_id = int(os.getenv("CHANNEL_ID"))

bot = ClappyBoy(command_prefix="", intents=discord.Intents.all(), channel_id=channel_id)
bot.run(token)
