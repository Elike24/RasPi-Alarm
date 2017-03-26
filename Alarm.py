from datetime import datetime
from enum import Enum


class Alarm:
    repeated = False
    days = Day.getfromint(datetime.today().weekday())

    def __init__(self, repeated: bool, days: Day, hour, minute, song: str, duration=3, enabled: bool = True):
        self.repeated = repeated
        self.days = days
        self.hour = hour
        self.minute = minute
        self.enabled = enabled
        self.song = song
        self.duration = duration

    def should_ring(self) -> bool:
        return self.enabled


class Day(Enum):  # replace Enum with Flag once using Python 3.6
    Mo = 1
    Tu = 2
    We = 4
    Th = 8
    Fr = 16
    Sa = 32
    Su = 64

    @staticmethod
    def get_from_int(weekday: int):
        return {
            0: Day.Mo,
            1: Day.Tu,
            2: Day.We,
            3: Day.Th,
            4: Day.Fr,
            5: Day.Sa,
            6: Day.Su
        }.get(weekday, Day.Mo)

    @staticmethod
    def everyday():
        return Day.Mo | Day.Tu | Day.We | Day.Th | Day.Fr | Day.Sa | Day.Su
