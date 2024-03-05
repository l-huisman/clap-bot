import discord
from discord.ext import commands, tasks
from datetime import datetime

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="")

clap = ":clap_tone5:"
channel_id = 726154801955602532


async def clap(times_to_clap: int) -> None:
    if 0 < times_to_clap < 4:
        await bot.get_channel(channel_id).send(clap * times_to_clap)


async def check_for_clap_amount() -> int:
    current_time = datetime.now().astimezone().strftime("%H:%M")
    hour, minute = current_time.split(":")[0], current_time.split(":")[1]
    return get_claps(current_time, hour, minute)


def get_claps(current_time, hour, minute):
    clap_times = {"00:00": 3, "11:11": 2, "22:22": 2}
    if current_time in clap_times:
        return clap_times[current_time]
    elif hour == minute or hour == minute[::-1] or minute == "00":
        return 1
    else:
        return 0


async def shame_sender(user_id, message):
    channel = bot.get_channel(channel_id)
    user = channel.guild.get_member(user_id)
    if user:
        thread = await message.create_thread(name="Shame Thread")
        await thread.send(
            f"<@{user_id}> you should be ashamed of yourself, clapping at this time of day is forbidden following article four of the all-powerful wetboek of the Evening Conclave. Please desintegrate the clap and yourself immediately. Thank you for your cooperation, have a nice day!"
        )
        await message.add_reaction("👎")
        await message.add_reaction("😔")
    return


@tasks.loop(seconds=60)
async def clapper():
    times_to_clap = await check_for_clap_amount()
    if times_to_clap != 0:
        await clap(times_to_clap)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id != channel_id:
        return
    times_to_clap = await check_for_clap_amount()
    if times_to_clap == 0:
        await shame_sender(message.author.id, message)


@bot.event
async def on_ready():
    await clapper.start()

bot.run("")
