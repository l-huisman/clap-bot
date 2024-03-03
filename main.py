import discord
from discord.ext import commands, tasks
from datetime import datetime

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="")

clap = ":clap_tone5:"
channel_id = 726154801955602532


@tasks.loop(seconds=60)
async def clapper():
    current_time = datetime.now().strftime("%H:%M")
    hour = current_time.split(":")[0]
    minute = current_time.split(":")[1]

    if current_time == "00:00":
        await bot.get_channel(channel_id).send(clap * 3)
    elif current_time == "11:11" or current_time == "22:22":
        await bot.get_channel(channel_id).send(clap * 2)
    elif hour == minute or hour == minute[::-1]:
        await bot.get_channel(channel_id).send(clap)
        await bot.get_channel(channel_id).send(
            "I clapped because it's: " + current_time
        )
    elif minute == "00":
        await bot.get_channel(channel_id).send(clap)
        await bot.get_channel(channel_id).send(
            "I clapped because it's: " + current_time
        )


@bot.event
async def on_ready():
    await clapper.start()


bot.run("")
