from github import Github
import os
import datetime
import time

# load token from GITHUB_TOKEN environment variable
token = os.environ["GITHUB_TOKEN"]


def main():
    g = Github(token)

    user = g.get_user("jerome3o")

    while True:
        all_events = list(user.get_events())
        push_events = [e for e in all_events if e.type == "PushEvent"]
        latest_event = max(push_events, key=lambda e: e.created_at)
        latest_event_time = latest_event.created_at

        # Check if latest push event happened today
        if latest_event_time.date() == datetime.date.today():
            print("Pushed today")

        time.sleep(10)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
