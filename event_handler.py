import discord

class EventHandler:

    def __init__(self, bot, channel_id: int, clap_message: str, message_manager, time_manager):
        self.__bot = bot
        self.__channel_id = channel_id
        self.__clap_message = clap_message
        self.__time_manager = time_manager
        self.__message_manager = message_manager

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.__bot.user:
            return
        if message.channel.id != self.__channel_id:
            return
        times_to_clap = await self.__bot.check_for_clap_amount()
        if times_to_clap == 0:
            await self.__message_manager.shame_sender(message.author.id, message)
        # TODO: Check if the message has the clap emoji

    async def on_message_delete(self, message: discord.Message) -> None:
        shame_message = self.__message_manager.get_shame_message()
        if message.channel.id != self.__channel_id:
            return
        if message == shame_message:
            return
        await self.__message_manager.remove_shame(shame_message)

    async def on_ready(self) -> None:
        await self.__bot.clapper.start()
