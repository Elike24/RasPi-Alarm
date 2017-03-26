import os
import time

from threading import Thread


class MplayerNotInstalledException(Exception):
    def __init__(self):
        print("Error: Mplayer required for playing alarm sounds\n")


class Mplayer(object):

    def __init__(self, pipedir: str, pipefile: str):
        self.running = False
        self.pipedir = pipedir
        self.pipefile = pipefile
        self.laststarted = None

    def start(self, songfile: str, duration: int) -> None:
        if self.running:
            self.stop()
            return
        self.running = True

        # create pipefile
        if not os.path.exists(self.pipedir):
            os.mkdir(self.pipedir)
        try:
            os.remove(self.pipefile)
        except OSError:
            pass  # file did not exist
        os.mkfifo(self.pipefile)

        # start player
        mplayer_options = "-really-quiet -slave -input file=\"%s\"" % self.pipefile
        playerthread = Thread(None, Mplayer.__runmplayer, "Alarm MPlayer thread", (mplayer_options, songfile))
        self.laststarted = time.time()
        playerthread.start()
        stopperthread = Thread(None, self.__stopplayer, "Alarm stopper thread", (duration, self.laststarted))
        stopperthread.start()

    @staticmethod
    def __runmplayer(options: str, song: str) -> None:
        os.system("mplayer %s \"%s\"" % (options, song))

    def __stopplayer(self, duration: int, started: float) -> None:
        time.sleep(duration)
        if self.laststarted == started:
            self.stop()

    def stop(self) -> None:
        if not self.running:
            return
        self.running = False

        # quit using pipefile
        if not os.path.exists(self.pipedir):
            os.mkdir(self.pipedir)
        with open(self.pipefile, "w") as stream:
            stream.write("quit\n")
            stream.close()
