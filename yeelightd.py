import subprocess
import time
import yeelight as yl

# Liv chose this colour bc she likes it
# {
#     "rgb": "16747178",
#     "bright": "80",
#     "ct": "3200",
#     "hul": "344",
#     "sat": "45",
# }


def _set_nice_colour(bulb: yl.Bulb) -> None:
    bulb.set_rgb(0xFF, 0x8A, 0xAA)
    bulb.set_brightness(80)
    bulb.set_color_temp(3200)
    bulb.set_hsv(344, 45)


def _set_red(bulb: yl.Bulb) -> None:
    bulb.set_rgb(0xFF, 0x00, 0x00)
    bulb.set_brightness(100)


def _set_yellow(bulb: yl.Bulb) -> None:
    bulb.set_rgb(0xFF, 0xFF, 0x00)
    bulb.set_brightness(100)


def _is_after_815pm() -> bool:
    now = time.localtime()
    return now.tm_hour == 20 and now.tm_min >= 15


def _is_playing_overwatch() -> bool:
    # use pgrep to look for processes matching "Overwatch"
    # look at the stdout of the command, if it's empty, return False
    # otherwise, return True

    # allow non-zero exit codes
    output = subprocess.run(["pgrep", "Overwatch"], capture_output=True, check=False).stdout != b""
    return output


def main():
    # get a list of all the bulbs on the network
    bulbs = yl.discover_bulbs()

    # look for IP of bulb with bulbs[i]['capabilities']['name'] == "jerome-pc-led"
    ip = next((b["ip"] for b in bulbs if b["capabilities"]["name"] == "jerome-pc-led"), None)

    if ip is None:
        print("Could not find bulb")
        return

    # create a Yeelight object
    bulb = yl.Bulb(ip)

    _last_red = False

    while True:
        _poll_time = 10
        is_playing_overwatch = _is_playing_overwatch()
        is_gettin_late = _is_after_815pm()

        if is_playing_overwatch:
            if is_gettin_late:
                _poll_time = 1
                if _last_red:
                    _set_yellow(bulb)
                    _last_red = False
                else:
                    _set_red(bulb)
                    _last_red = True
            else:
                _set_red(bulb)

        else:
            _set_nice_colour(bulb)

        time.sleep(_poll_time)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
