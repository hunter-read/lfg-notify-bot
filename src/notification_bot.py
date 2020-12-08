import praw
import prawcore
import time
import json
import re
import sys
from redis import Redis
from logging import Logger
from service import init_logger
from model import Database, UserRequest

__reddit: praw.Reddit = praw.Reddit("notification" + sys.argv[1])
__logger: Logger = init_logger("notification_bot", __reddit)
__redis: Redis = Redis()


def message_user(db: Database, data: dict) -> None:
    username = data['username']
    message = data['message']
    if __reddit.config.custom["environment"] != "production":
        __logger.info(f"Recieved message for {username}")
        return

    try:
        __reddit.redditor(username).message('New LFG post matching your criteria', message)

    except praw.exceptions.RedditAPIException as err:

        match = re.search(r"(\d+)\s(minute|millisecond|second)", str(err))

        if "RATELIMIT" in str(err) and match:
            sleep_time = int(match.group(1)) + 1
            if match.group(2) == "minute":
                sleep_time = (sleep_time * 60)
            if match.group(2) == "millisecond":
                sleep_time = 1
            __logger.warning(f"RATELIMIT. Waiting {sleep_time} seconds")
            time.sleep(sleep_time)
        else:
            __logger.error(f"Api Error: {err}")
            time.sleep(30)

    except prawcore.exceptions.ServerError as err:
        __logger.error(f"Server Error: {err}")
        time.sleep(30)

    else:
        UserRequest(username=username).update_notification_count()


def main():
    __logger.info("Starting notification bot")
    database = __reddit.config.custom["database"]
    if not database:
        __logger.error("Database location not set. Exiting")
        exit(1)

    with Database(database) as db:
        while True:
            message = __redis.blpop("lfg-notification")
            if message:
                data = json.loads(message[1].decode("utf-8"))
                message_user(db, data)


if __name__ == "__main__":
    main()
