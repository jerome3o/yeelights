import requests
from bs4 import BeautifulSoup
import datetime


def has_commited_today(user: str) -> bool:
    url = f"https://github.com/users/{user}/contributions"

    # add cookie tz=Pacific%2FAuckland
    r = requests.get(url, headers={"Cookie": "tz=Pacific%2FAuckland"})

    # handle error
    if r.status_code != 200:
        raise Exception(f"Error: {r.status_code}")

    soup = BeautifulSoup(r.content.decode("utf-8"), "html.parser")

    # get todays date in 2023-06-23 format
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # get tr element with data-date=today
    todays_contrib = soup.find("rect", {"data-date": today}).attrs["data-level"]
    return todays_contrib != "0"
