class Alarm:

    def __init__(self, repeated, days, hour, minute, song, enabled):
        self.repeated = repeated
        self.days = days
        self.hour = hour
        self.minute = minute
        self.enabled = enabled
        self.song = song

    def shouldring(self):
        return self.enabled
