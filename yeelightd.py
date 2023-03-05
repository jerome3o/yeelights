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
    bulb.set_rgb(16747178)
    bulb.set_brightness(80)
    bulb.set_color_temp(3200)
    bulb.set_hsv(344, 45)



def _playing_overwatch() -> bool:
    # use pgrep to look for processes matching "Overwatch"
    # look at the stdout of the command, if it's empty, return False
    # otherwise, return True
    output = subprocess.check_output(["pgrep", "Overwatch"]) != b""
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
    bulb = yl.Yeelight(ip)

    is_playing_overwatch = _playing_overwatch()




if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
