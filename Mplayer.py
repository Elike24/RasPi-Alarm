import time
from datetime import timedelta, datetime
from threading import Thread

import vlc


class Mplayer(object):
    def __init__(self):
        self.running = False
        self.player = None
        self.last_started = None

    def start(self, song_file: str, duration: timedelta) -> None:
        if self.running:
            self.stop()
        self.running = True

        # start player
        self.player = vlc.MediaPlayer(song_file, 'input-repeat=-1')
        self.player.play()

        # stop player later
        stopper_thread = Thread(None, self.__stop_player, "Alarm stopper thread", (duration, self.last_started))
        stopper_thread.start()

    def __stop_player(self, duration: timedelta, started: datetime) -> None:
        for slept in range(0, int(duration.total_seconds())):
            time.sleep(1)
            if not self.running or not self.last_started == started:
                return
        self.stop()

    def stop(self) -> None:
        if not self.running:
            return

        self.player.stop()
        self.running = False
