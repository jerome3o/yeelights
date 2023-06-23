import yeelight as yl
import os

_LED_IP = os.environ.get("YEELIGHT_IP", None)
_LAMP_IP = os.environ.get("YEELIGHT_LAMP_IP", None)


def main():
    b = yl.Bulb(_LED_IP)
    lamp = yl.Bulb(_LAMP_IP)
    b.turn_off()
    lamp.turn_off()


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
