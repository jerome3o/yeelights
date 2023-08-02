import os
import datetime
import requests

from bs4 import BeautifulSoup

access_token = os.getenv("GITHUB_TOKEN")


def has_commited_today(user: str) -> bool:
    url = f"https://github.com/users/{user}/contributions"

    cookie = """tz=Pacific%2FAuckland"""

    r = requests.get(
        url,
        headers={
            "Cookie": cookie,
            "Authorization": f"bearer {access_token}",
            "Cache-Control": "no-cache",
        },
    )

    # handle error
    if r.status_code != 200:
        raise Exception(f"Error: {r.status_code}")

    soup = BeautifulSoup(r.content.decode("utf-8"), "html.parser")

    # get todays date in 2023-06-23 format
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # get tr element with data-date=today
    tr_element = soup.find(None, {"data-date": today})
    todays_contrib = tr_element.get("data-level")
    return todays_contrib != "0"


def main():
    print(has_commited_today("jerome3o"))


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
