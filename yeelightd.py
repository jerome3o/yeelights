import subprocess
import os
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

_name = os.environ.get("YEELIGHT_NAME", "Sam")
_ip = os.environ.get("YEELIGHT_IP", None)
_lamp_ip = os.environ.get("YEELIGHT_LAMP_IP", None)
_poll_time = 10


def _is_weekend() -> bool:
    now = time.localtime()
    # check if it's friday or saturday
    return now.tm_wday == 4 or now.tm_wday == 5


def _set_nice_colour(bulb: yl.Bulb) -> None:
    bulb.turn_on()
    bulb.set_rgb(0xFF, 0x8A, 0xAA)
    bulb.set_brightness(80)
    bulb.set_color_temp(3200)
    bulb.set_hsv(344, 45)


def _set_red(bulb: yl.Bulb) -> None:
    bulb.turn_on()
    bulb.set_rgb(0xFF, 0x00, 0x00)
    bulb.set_brightness(100)


def _set_yellow(bulb: yl.Bulb) -> None:
    bulb.turn_on()
    # bulb.set_rgb(0xFF, 0xFF, 0x00)
    bulb.set_rgb(0x00, 0x00, 0xFF)
    bulb.set_brightness(100)


def _is_after_830pm() -> bool:
    now = time.localtime()
    return now.tm_hour >= 20 and now.tm_min >= 30


def _is_after_10pm() -> bool:
    now = time.localtime()
    return now.tm_hour >= 22


def _is_playing_overwatch() -> bool:
    # use pgrep to look for processes matching "Overwatch"
    # look at the stdout of the command, if it's empty, return False
    # otherwise, return True

    # allow non-zero exit codes
    output = (
        subprocess.run(
            ["pgrep", "Overwatch"],
            capture_output=True,
            check=False,
        ).stdout
        != b""
    )
    return output


def _red_yellow_flash(bulb: yl.Bulb, _last_red: bool) -> bool:
    if _last_red:
        _set_yellow(bulb)
        return False

    _set_red(bulb)
    return True


def main():
    # get a list of all the bulbs on the network
    bulbs = yl.discover_bulbs()

    # look for IP of bulb with bulbs[i]['capabilities']['name'] == _name
    ip = next(
        (b["ip"] for b in bulbs if b["capabilities"]["name"] == _name),
        None,
    )

    if _ip is not None:
        print("Using IP from environment variable")
        ip = _ip

    if ip is None:
        print("Could not find bulb")
        return

    # create a Yeelight object
    bulb = yl.Bulb(ip)
    lamp = yl.Bulb(_lamp_ip)
    print(bulb)
    print(lamp)

    _last_red = False

    while True:
        if _is_playing_overwatch():
            if (_is_after_830pm() and not _is_weekend()) or (
                _is_after_10pm() and not _is_weekend()
            ):
                _last_red = _red_yellow_flash(bulb, _last_red)
            else:
                _set_red(bulb)
        else:
            _set_nice_colour(bulb)
        time.sleep(_poll_time)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
