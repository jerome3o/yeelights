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
