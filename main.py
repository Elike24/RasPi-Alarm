import os
import re
import sys
import tempfile
from datetime import timedelta
from os import path
from random import choice

from Mplayer import Mplayer

__all__ = "alarm"
__author__ = "Elias Keis"
__version_info__ = (0, 1)
__version__ = "{0}.{1}".format(*__version_info__)
__license__ = "GNU General Public License v3 (GPLv3)"


# noinspection PyUnresolvedReferences
def add_gpio_listener(pin_nr, callback, bounce_time=200):
    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_nr, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(pin_nr, GPIO.FALLING, callback=callback, bouncetime=bounce_time)
    except RuntimeError:
        print_help("Failed to add pin listener, are we on an Raspberry Pi? If not, use --no-gpio!")
        return


def parse_time(time_str):
    regex = re.compile(r'((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for (name, param) in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)


def print_help(error: str = "") -> None:
    if not error == "":
        print(error + "\n")
    print("Plays a sound for given time. Can stop playing when getting an event from GPIO pins.\n\n" +
          "Parameters (all optional):\n" +
          "--version\t-v\tprint version\n" +
          "--help\t\t-h\tprint this message\n" +
          "--song <s>\t-s <s>\tplays sound from file stored at <s>\n" +
          "--playlist <p>\t-p <p>\tplays random sound from playlist stored at <p>\n" +
          "--duration <t>\t-d <t>\thow long the song is played (default 5min).\n" +
          "\t\t\tExamples: 5s, 3h:4min:2s, ...\n" +
          "--no-gpio\t\tDisables GPIO-Pins\n" +
          "--pin <p>\t-p <p>\tNumber of the GPIO-Pin to use")


def songs_in_playlist(playlist):
    songs = []
    with open(playlist) as f:
        for line in f.readlines():
            song = line.strip()
            if not path.isabs(song):
                song = path.join(path.dirname(playlist), song)
            songs.append(song)
    return songs


def main() -> None:
    args = sys.argv
    args.pop(0)

    alarm_sounds = []
    alarm_duration = timedelta(minutes=5)
    no_gpio = False
    pin_nr = 7

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
                alarm_sounds.append(args[cur_arg_i])
                cur_arg_i += 1
        elif cur_arg == "--playlist" or cur_arg == "-p":
            if cur_arg_i >= len(args):
                print_help("Missing argument: playlist file")
                return
            else:
                alarm_playlist = args[cur_arg_i]
                cur_arg_i += 1
                try:
                    alarm_sounds.extend(songs_in_playlist(alarm_playlist))
                except IOError:
                    print_help("Invalid playlist file")
        elif cur_arg == "--duration" or cur_arg == "-d":
            if cur_arg_i >= len(args):
                print_help("Missing argument: duration")
                return
            else:
                alarm_duration = parse_time(args[cur_arg_i])
                cur_arg_i += 1
        elif cur_arg == "--no-gpio":
            no_gpio = True
        elif cur_arg == "--pin" or cur_arg == "-p":
            if cur_arg_i >= len(args):
                print_help("Missing argument: pin number")
                return
            else:
                pin_nr = int(args[cur_arg_i])
                cur_arg_i += 1
        else:
            print_help("Unknown parameter '%s'" % cur_arg)
            return

    if len(alarm_sounds) < 1:
        print_help("You should provide at least one song or playlist file")
        return

    alarm_sound = choice(alarm_sounds)

    pipe_dir = tempfile.mkdtemp("", "AlarmMPlayerPipe")
    pipe_file = os.path.join(pipe_dir, "pipe")
    player = Mplayer()
    player.start(alarm_sound, alarm_duration)

    if not no_gpio:
        def got_pin_input(changed_pin):
            if changed_pin == pin_nr:
                player.stop()
        add_gpio_listener(pin_nr, got_pin_input)
    try:
        import time
        while player.running:
            time.sleep(1)
    except KeyboardInterrupt:
        player.stop()
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
