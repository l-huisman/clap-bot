import discord
from time_manager import TimeManager
from event_handler import EventHandler
from discord.ext import commands, tasks
from message_manager import MessageManager


class ClappyBoy(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, channel_id: int):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.__channel_id = channel_id
        self.__time_manager = TimeManager()
        self.__clap_message = ":clap_tone5:"
        self.__event_handler = EventHandler(self, self.__channel_id, self.__message_manager)
        self.__message_manager = MessageManager(self, self.__channel_id, self.__clap_message)

    async def check_for_clap_amount(self) -> int:
        current_time = self.__time_manager.get_current_time()
        hour, minute = current_time.split(":")[0], current_time.split(":")[1]
        return self.__time_manager.get_claps(current_time, hour, minute)

    @tasks.loop(seconds=1)
    async def clapper(self):
        if self.__time_manager.clapped_this_minute():
            return
        times_to_clap = await self.check_for_clap_amount()
        if times_to_clap != 0:
            await self.__message_manager.clap(times_to_clap)

    async def on_message(self, message: discord.Message) -> None:
        await self.__event_handler.on_message(message)

    async def on_message_delete(self, message: discord.Message) -> None:
        await self.__event_handler.on_message_delete(message)

    async def on_ready(self) -> None:
        await self.__event_handler.on_ready()