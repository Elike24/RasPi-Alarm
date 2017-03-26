class Alarm:

    def __init__(self, repeated: bool, days, hour, minute, song: str, duration=3, enabled: bool = True):
        self.repeated = repeated
        self.days = days
        self.hour = hour
        self.minute = minute
        self.enabled = enabled
        self.song = song
        self.duration = duration

    def shouldring(self) -> bool:
        return self.enabled
