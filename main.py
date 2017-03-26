import os
import sys
import tempfile
import time

from Alarm import Alarm
from Mplayer import Mplayer

__all__ = "alarm"
__author__ = "Elias Keis"
__version_info__ = (0, 1)
__version__ = "{0}.{1}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"
__email__ = "elias.keis@freenet.de"


alarms = [Alarm(True, "", "", "", "/home/elias/Musik/Alarm.mp3", True)]
pipedir = tempfile.mkdtemp("", "AlarmMPlayerPipe")
pipefile = os.path.join(pipedir, "pipe")
player = Mplayer(tempfile.gettempdir(), pipefile)


def waitforalarms():
    while True:
        for alarm in alarms:
            if alarm.shouldring():
                print("Ringing alarm!")
                player.start(alarm.song)
                if not alarm.repeated:
                    alarms.remove(alarm)
                time.sleep(3)
                player.stop()
        time.sleep(3)


def printhelp(error=""):
    if not error == "":
        print(error + "\n\n")
    print("-" * 5 + " HELP " + "-" * 5 + "\n")
    print("This program does nothing\n")


def main():
    args = sys.argv
    args.pop(0)
    if len(args) == 0:
        print("Waiting for alarms to ring...")
        waitforalarms()
    elif len(args) == 1 and args[0] == "-h" or args[0] == "--help":
        printhelp()
    elif len(args) == 1 and args[0] == "-v" or args[0] == "--version":
        print("Version : %s" % __version__)
    else:
        printhelp("Unknown command")
    player.stop()
    os.remove(pipefile)
    os.rmdir(pipedir)


if __name__ == "__main__":
    main()
