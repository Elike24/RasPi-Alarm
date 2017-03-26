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


alarms = [Alarm(True, "", "", "", "/home/elias/Musik/Alarm.mp3")]
# Alarm(True, "", "", "", "/home/elias/Musik/Alarm2.mp3")

pipedir = tempfile.mkdtemp("", "AlarmMPlayerPipe")
pipefile = os.path.join(pipedir, "pipe")
player = Mplayer(tempfile.gettempdir(), pipefile)


def waitforalarms() -> None:
    try:
        while True:
            for alarm in alarms:
                if alarm.shouldring():
                    print("Ringing alarm!")
                    player.start(alarm.song, alarm.duration)
                    if not alarm.repeated:
                        alarms.remove(alarm)
            time.sleep(6)
    except KeyboardInterrupt:
        return


def printhelp(error: str = "") -> None:
    if not error == "":
        print(error + "\n")
    print("-" * 5 + " HELP " + "-" * 5 + "\n")
    print("This program is not doing much so far ...\n")


def main() -> None:
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
    try:
        os.remove(pipefile)
    except OSError:
        pass  # file did not exist
    os.rmdir(pipedir)


if __name__ == "__main__":
    main()
