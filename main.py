import os
import sys
import tempfile

from Alarm import *
from Mplayer import Mplayer

__all__ = "alarm"
__author__ = "Elias Keis"
__version_info__ = (0, 1)
__version__ = "{0}.{1}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"


def print_help(error: str = "") -> None:
    if not error == "":
        print(error + "\n")
    print("-" * 5 + " HELP " + "-" * 5 + "\n")
    print("This program is not doing much so far ...\n")


def main() -> None:
    args = sys.argv
    args.pop(0)

    song = Alarm.song_default
    duration = Alarm.duration_default
    cur_arg_i = 0
    while cur_arg_i < len(args):
        cur_arg = args[cur_arg_i]
        cur_arg_i += 1
        if cur_arg == "--version" or cur_arg == "-v":
            print("Version: %s" % __version__)
            return
        elif cur_arg == "--help" or cur_arg == "-h":
            print_help()
            return
        elif cur_arg == "--song" or cur_arg == "-s":
            if cur_arg_i >= len(args):
                print_help("Missing argument: song file")
                return
            else:
                song = args[cur_arg_i]
                cur_arg_i += 1
        elif cur_arg == "--duration" or cur_arg == "-d":
            if cur_arg_i >= len(args):
                print_help("Missing argument: duration")
                return
            else:
                duration = Alarm.parse_time(args[cur_arg_i])
                cur_arg_i += 1
        else:
            print_help("Unknown parameter '%s'" % cur_arg)
            return

    pipe_dir = tempfile.mkdtemp("", "AlarmMPlayerPipe")
    pipe_file = os.path.join(pipe_dir, "pipe")
    player = Mplayer(tempfile.gettempdir(), pipe_file)
    player.start(song, duration)

    try:
        while player.running:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    try:
        os.remove(pipe_file)
    except OSError:
        pass  # file did not exist
    try:
        os.rmdir(pipe_dir)
    except OSError:
        pass  # dir did not exist


if __name__ == "__main__":
    main()
