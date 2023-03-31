import yeelight as yl

_NAME = "Sam"
_IP = "192.168.1.15"

def main():
    b = yl.Bulb(_IP)
    b.turn_off()


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    main()
