import os
import sys
import tempfile

from Alarm import *
from AlarmClock import AlarmClock
from Mplayer import Mplayer

__all__ = "alarm"
__author__ = "Elias Keis"
__version_info__ = (0, 1)
__version__ = "{0}.{1}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"
__email__ = "elias.keis@freenet.de"


pipe_dir = tempfile.mkdtemp("", "AlarmMPlayerPipe")
pipe_file = os.path.join(pipe_dir, "pipe")
player = Mplayer(tempfile.gettempdir(), pipe_file)


def print_help(error: str = "") -> None:
    if not error == "":
        print(error + "\n")
    print("-" * 5 + " HELP " + "-" * 5 + "\n")
    print("This program is not doing much so far ...\n")


def main() -> None:
    args = sys.argv
    args.pop(0)
    if len(args) == 0:
        print("Waiting for alarms to ring...")
        clock = AlarmClock(player, [Alarm(duration=timedelta(seconds=3),
                                          time=(datetime.now() + timedelta(seconds=12)).time()),
                                    Alarm(duration=timedelta(seconds=3)),
                                    Alarm(time=(datetime.now() + timedelta(seconds=10)).time(),
                                          song="/home/elias/Musik/Alarm2.mp3", duration=timedelta(seconds=10))])
        try:
            while clock.handle_next_alarm():
                pass
        except KeyboardInterrupt:
            player.stop()
            print("Bye!\n")
    elif len(args) == 1 and args[0] == "-h" or args[0] == "--help":
        print_help()
    elif len(args) == 1 and args[0] == "-v" or args[0] == "--version":
        print("Version : %s" % __version__)
    else:
        print_help("Unknown command")

    while player.running:
        pass
    try:
        os.remove(pipe_file)
    except OSError:
        pass  # file did not exist
    os.rmdir(pipe_dir)


if __name__ == "__main__":
    main()
