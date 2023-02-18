import yeelight as yl


def main():
    devices = yl.discover_bulbs()
    for device in devices:
        b = yl.Bulb(device["ip"])
        b.turn_on()
        b.set_brightness(100)
        print(b.get_properties())
        b.set_name("jerome-pc-led")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
