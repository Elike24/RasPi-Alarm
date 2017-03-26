import os
import time

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

    def start(self, song_file: str, duration: int) -> None:
        if self.running:
            self.stop()
            return
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
        player_thread = Thread(None, Mplayer.__run_mplayer, "Alarm MPlayer thread", (mplayer_options, song_file))
        self.last_started = time.time()
        player_thread.start()
        stopper_thread = Thread(None, self.__stop_mplayer, "Alarm stopper thread", (duration, self.last_started))
        stopper_thread.start()

    @staticmethod
    def __run_mplayer(options: str, song: str) -> None:
        os.system("mplayer %s \"%s\"" % (options, song))

    def __stop_mplayer(self, duration: int, started: float) -> None:
        time.sleep(duration)
        if self.last_started == started:
            self.stop()

    def stop(self) -> None:
        if not self.running:
            return
        self.running = False

        # quit using pipe file
        if not os.path.exists(self.pipe_dir):
            os.mkdir(self.pipe_dir)
        with open(self.pipe_file, "w") as stream:
            stream.write("quit\n")
            stream.close()
