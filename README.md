# Yeelight automation

I have a yeelight-strip-8, this repo is POC for python automation of the LED strip.

## Setup

### Linux

```sh
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Usage

This will use the `SSDP` protocol on port 1892 (yeelight's specific SSDP setup) to find all yeelight bulbs on your network and then do something with them - at the moment just turn them on.

```sh
python main.py
```

### Automatic on/off (linux only, tested on arch + gnome + xorg)

Update the systemd units in `./systemd_units/` to fit with your code location, then copy them to `/etc/systemd/system`

so something like:

```sh
sudo cp ./systemd_units/ /etc/systemd/system
sudo systemctl enable yeelightd
sudo systemctl enable yeelightsoff
sudo systemctl start yeelightd
sudo systemctl start yeelightsoff
```

