import re
from datetime import timedelta


class Alarm:
    song_default = "/home/elias/Musik/Alarm.mp3"
    duration_default = timedelta(minutes=5)

    def __init__(self, song: str = song_default, duration: timedelta = duration_default):
        self.song = song
        self.duration = duration

    @staticmethod
    def parse_time(time_str):
        regex = re.compile(r'((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
        parts = regex.match(time_str)
        if not parts:
            return
        parts = parts.groupdict()
        time_params = {}
        for (name, param) in parts.items():
            if param:
                time_params[name] = int(param)
        return timedelta(**time_params)
