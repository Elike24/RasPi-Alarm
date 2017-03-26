import os

from threading import Thread


class MplayerNotInstalledException(Exception):
    def __init__(self):
        print("Error: Mplayer required for playing alarm sounds\n")


class Mplayer(object):

    def __init__(self, pipedir, pipefile):
        self.running = False
        self.pipedir = pipedir
        self.pipefile = pipefile

    def start(self, songfile):
        if self.running:
            print("Alarm is already running!\n")
            return
        self.running = True

        # create pipefile
        if not os.path.exists(self.pipedir):
            os.mkdir(self.pipedir)
        try:
            os.remove(self.pipefile)
        except OSError:
            pass
        os.mkfifo(self.pipefile)

        # start player
        mplayer_options = "-really-quiet -slave -input file=\"%s\"" % self.pipefile
        thread = Thread(None, Mplayer.__runmplayer, "Alarm MPlayer thread", (mplayer_options, songfile))
        thread.start()
        print("Alarm started!")

    @staticmethod
    def __runmplayer(options, song):
        os.system("mplayer %s \"%s\"" % (options, song))

    def stop(self):
        if not self.running:
            print("No alarm running!\n")
            return
        self.running = False
        print("Stopping alarm...")

        # quit using pipefile
        if not os.path.exists(self.pipedir):
            os.mkdir(self.pipedir)
        with open(self.pipefile, "w") as stream:
            stream.write("quit\n")
            stream.close()
