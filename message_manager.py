import random
import discord

from discord.ext import commands


class MessageManager:

    def __init__(self, bot: commands.Bot, channel_id: int, clap_message: str):
        self.__bot = bot
        self.__shame_messages = []
        self.__channel_id = channel_id
        self.__clap_message = clap_message
        self.__emoji_list = ["👎", "😔", "👀", "🤔", "😂", "🙌", "🔥"]

    async def clap(self, times_to_clap: int) -> None:
        if 0 < times_to_clap < 4:
            await self.__bot.get_channel(self.__channel_id).send(
                (self.__clap_message + " ") * times_to_clap
            )

    async def shame_sender(self, user_id: int, user_message: discord.Message) -> None:
        user = self.__bot.get_user(user_id)
        if user:
            self.__shame_message = await self.__bot.get_channel(self.__channel_id).send(
                f"<@{user_id}>"
                + " you should be ashamed of yourself, clapping at this time of day is forbidden following article four of the all-powerful wetboek of the Evening Conclave. Please desintegrate the clap and yourself immediately. Thank you for your cooperation, have a nice day!"
            )
            for emoji in self.__emoji_list:
                await user_message.add_reaction(emoji)
        return

    def get_shame_message(self) -> discord.Message:
        return self.__shame_message

    def get_random_shame_message(self) -> discord.Message:
        return random.choice(self.__shame_messages)

    async def remove_shame(self, message: discord.Message) -> None:
        await message.delete()
