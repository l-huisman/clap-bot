import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
channel_id = int(os.getenv("CHANNEL_ID"))

# ClapBot Class


class ClappyBoy(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.clap_message = ":clap_tone5:"
        self.shame_message = None

    async def clap(self, times_to_clap: int) -> None:
        if 0 < times_to_clap < 4:
            await self.get_channel(channel_id).send(
                (self.clap_message + " ") * times_to_clap
            )

    async def check_for_clap_amount(self) -> int:
        current_time = datetime.now().astimezone(tz=pytz.timezone('Europe/Amsterdam')).strftime("%H:%M")
        hour, minute = current_time.split(":")[0], current_time.split(":")[1]
        return self.get_claps(current_time, hour, minute)

    def get_claps(self, current_time, hour, minute):
        clap_times = {"00:00": 3, "11:11": 2, "22:22": 2}
        if current_time in clap_times:
            return clap_times[current_time]
        elif hour == minute or hour == minute[::-1] or minute == "00":
            return 1
        else:
            return 0

    async def shame_sender(self, user_id, user_message):
        user = self.get_user(user_id)
        if user:
            message = await self.get_channel(channel_id).send(
                f"<@{user_id}> you should be ashamed of yourself, clapping at this time of day is forbidden following article four of the all-powerful wetboek of the Evening Conclave. Please desintegrate the clap and yourself immediately. Thank you for your cooperation, have a nice day!"
            )
            self.shame_message = message
            emoji_list = [
                "👎",
                "😔",
                "👀",
                "🤔",
                "😂",
                "🙌",
                "🔥",
                # ":rage:",
                # ":face_with_symbols_over_mouth:",
                # ":face_with_raised_eyebrow:",
                # ":face_vomiting:",
                # ":pouting_cat:",
                # ":scream:",
                # ":angry:",
            ]
            for emoji in emoji_list:
                await user_message.add_reaction(emoji)
        return

    async def remove_shame(self, message):
        await message.delete()

    @tasks.loop(seconds=60)
    async def clapper(self):
        times_to_clap = await self.check_for_clap_amount()
        if times_to_clap != 0:
            await self.clap(times_to_clap)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.channel.id != channel_id:
            return
        times_to_clap = await self.check_for_clap_amount()
        if times_to_clap == 0:
            await self.shame_sender(message.author.id, message)
        # TODO: Check if the message has the clap emoji

    async def on_message_delete(self, message):
        if message.channel.id != channel_id:
            return
        if message == self.shame_message:
            return
        await self.remove_shame(self.shame_message)

    async def on_ready(self):
        await self.clapper.start()


bot = ClappyBoy(command_prefix="", intents=discord.Intents.all())

bot.run(token)
