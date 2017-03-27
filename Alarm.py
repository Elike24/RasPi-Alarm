from datetime import datetime, timedelta

from Day import Day


class Alarm:
    repeated = False
    song_default = "/home/elias/Musik/Alarm.mp3"

    def __init__(self, days: Day = Day.get_from_int(datetime.today().weekday()),
                 time: datetime.time = (datetime.now() + timedelta(seconds=2)).time(),
                 song: str = song_default, repeated: bool = False, duration: timedelta = timedelta(minutes=5),
                 enabled: bool = True):
        self.repeated = repeated
        self.days = days
        self.time = time
        self.enabled = enabled
        self.song = song
        self.duration = duration

    def next_ring(self) -> datetime or None:
        if (not self.days) or (not self.enabled):
            return None

        ring_time = datetime.now()
        # set microseconds
        if ring_time.microsecond > self.time.microsecond:
            ring_time += timedelta(seconds=1)
        ring_time = ring_time.replace(microsecond=self.time.microsecond)
        # set seconds
        if ring_time.second > self.time.microsecond:
            ring_time += timedelta(minutes=1)
        ring_time = ring_time.replace(second=self.time.second)
        # set minutes
        if ring_time.minute > self.time.minute:
            ring_time += timedelta(hours=1)
        ring_time = ring_time.replace(minute=self.time.minute)
        # set hour
        if ring_time.hour > self.time.hour:
            ring_time += timedelta(days=1)
        ring_time = ring_time.replace(hour=self.time.hour)
        # set day
        while not self.days & Day.get_from_int(ring_time.weekday()):
            ring_time += timedelta(days=1)
        return ring_time

    def next_ring_or_max(self) -> datetime:
        ring_time = self.next_ring()
        if ring_time is None:
            ring_time = datetime.max
        return ring_time

    def __lt__(self, other) -> bool:
        assert isinstance(other, Alarm) or isinstance(other, datetime)
        if isinstance(other, Alarm):
            other_time = other.next_ring_or_max()
        else:
            other_time = other
        return self.next_ring_or_max() < other_time

    def __le__(self, other) -> bool:
        assert isinstance(other, Alarm) or isinstance(other, datetime)
        if isinstance(other, Alarm):
            other_time = other.next_ring_or_max()
        else:
            other_time = other
        return self.next_ring_or_max() <= other_time

    def __ge__(self, other) -> bool:
        assert isinstance(other, Alarm) or isinstance(other, datetime)
        if isinstance(other, Alarm):
            other_time = other.next_ring_or_max()
        else:
            other_time = other
        return self.next_ring_or_max() >= other_time

    def __gt__(self, other) -> bool:
        assert isinstance(other, Alarm) or isinstance(other, datetime)
        if isinstance(other, Alarm):
            other_time = other.next_ring_or_max()
        else:
            other_time = other
        return self.next_ring_or_max() > other_time

