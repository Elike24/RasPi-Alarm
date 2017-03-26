import time
from datetime import datetime

from typing import List

from Alarm import Alarm
from Mplayer import Mplayer


class AlarmClock:
    def __init__(self, player: Mplayer, alarms: List[Alarm] = None):
        self.player = player
        if alarms is None:
            self.alarms = []
        else:
            self.alarms = alarms

    def handle_next_alarm(self) -> bool:
        next_alarm_time = None
        next_alarm = None
        self.alarms.sort(key=Alarm.next_ring)
        for alarm in self.alarms:
            next_alarm_time = alarm.next_ring()
            if next_alarm_time is not None:
                next_alarm = alarm
                break
        if next_alarm is None:
            return False

        print("Next alarm in " + str(next_alarm_time - datetime.now()))
        time.sleep((next_alarm_time - datetime.now()).total_seconds())
        self.player.start(next_alarm.song, next_alarm.duration)
        if not next_alarm.repeated:
            next_alarm.enabled = False
        return True
