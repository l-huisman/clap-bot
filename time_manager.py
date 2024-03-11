import pytz
from datetime import datetime


class TimeManager:
    def __init__(self) -> None:
        self.__clapped_minute = self.get_current_time()

    def get_current_time(self):
        current_time = datetime.now().astimezone(tz=pytz.timezone("Europe/Amsterdam"))
        return current_time.strftime("%H:%M")

    def get_claps(self, current_time, hour, minute):
        clap_times = {"00:00": 3, "11:11": 2, "22:22": 2}
        if current_time in clap_times:
            return clap_times[current_time]
        elif hour == minute or hour == minute[::-1] or minute == "00":
            return 1
        else:
            return 0

    def clapped_this_minute(self) -> bool:
        current_time = self.get_current_time()
        if current_time != self.__clapped_minute:
            self.__clapped_minute = current_time
            return False
        return True
