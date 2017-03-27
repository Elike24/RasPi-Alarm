import os
import time
from datetime import timedelta, datetime

from threading import Thread


class MplayerNotInstalledException(Exception):
    def __init__(self):
        print("Error: Mplayer required for playing alarm sounds\n")


class Mplayer(object):
    def __init__(self, pipe_dir: str, pipe_file: str):
        self.running = False
        self.pipe_dir = pipe_dir
        self.pipe_file = pipe_file
        self.last_started = None

    def start(self, song_file: str, duration: timedelta) -> None:
        if self.running:
            self.stop()
        self.running = True

        # create pipe file
        if not os.path.exists(self.pipe_dir):
            os.mkdir(self.pipe_dir)
        try:
            os.remove(self.pipe_file)
        except OSError:
            pass  # file did not exist
        os.mkfifo(self.pipe_file)

        # start player
        mplayer_options = "-really-quiet -slave -input file=\"%s\"" % self.pipe_file
        self.last_started = datetime.now()
        player_thread = Thread(None, self.__run_mplayer, "Alarm MPlayer thread",
                               (mplayer_options, song_file, self.last_started))
        player_thread.start()
        stopper_thread = Thread(None, self.__stop_mplayer, "Alarm stopper thread", (duration, self.last_started))
        stopper_thread.start()

    def __run_mplayer(self, options: str, song: str, started: datetime) -> None:
        print("Playing alarm sound...")
        while self.running and self.last_started == started:
            result = os.system("mplayer %s \"%s\"" % (options, song))
            # 256 means KeyboardInterrupt
            if result != 0 and result != 256:
                print("Error %i when trying to play. Is mplayer installed?" % result)
                self.stop()

    def __stop_mplayer(self, duration: timedelta, started: datetime) -> None:
        time.sleep(duration.total_seconds())
        if self.last_started == started:
            print("Stopping alarm sound!")
            self.stop()
        else:
            print("Did not stop alarm sound, player is already playing next one")

    def stop(self) -> None:
        if not self.running:
            return

        # quit using pipe file
        if not os.path.exists(self.pipe_dir):
            os.mkdir(self.pipe_dir)
        with open(self.pipe_file, "w") as stream:
            stream.write("quit\n")
            stream.close()

        self.running = False
