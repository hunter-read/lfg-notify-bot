import os
import re
import time

import praw
import prawcore

from logging import Logger
from model import Database, Notification, Redis, User
from service import init_logger


__reddit: praw.Reddit = praw.Reddit("notification")
__logger: Logger = init_logger()
__redis: Redis = Redis()
__production: bool = os.environ.get('PROFILE') == "production"


def parse_API_exception(err: praw.exceptions.RedditAPIException) -> int:
    match = re.search(r"(\d+)\s(minute|millisecond|second)", str(err))

    if "RATELIMIT" in str(err) and match:
        sleep_time = int(match.group(1)) + 1
        if match.group(2) == "minute":
            sleep_time = (sleep_time * 60)
        if match.group(2) == "millisecond":
            sleep_time = 1
        __logger.warning(f"RATELIMIT. Waiting {sleep_time} seconds")
        return sleep_time
    elif "USER_DOESNT_EXIST" in str(err):
        __logger.info("User does not exist")
        return -1
    elif "NOT_WHITELISTED_BY_USER" in str(err):
        __logger.info("User has blocked bot")
        return -1
    elif "That user is invalid" in str(err):
        __logger.info("Invalid User.")
        return -1
    else:
        __logger.error(f"Api Error: {err}")
        return 30


def message_user(notification: Notification) -> int:
    if not __production:
        __logger.info(f"Recieved message for {notification.username}")
        return 0

    try:
        redditor = __reddit.redditor(notification.username)
        redditor.message(subject=notification.subject, message=notification.body)

    except prawcore.exceptions.Forbidden as err:
        __logger.error(f"Error sending message to {notification.username}: {err}")
        return 0

    except praw.exceptions.RedditAPIException as error:
        return parse_API_exception(error)

    except prawcore.exceptions.ServerError as err:
        __logger.error(f"Server Error: {err}")
        return 30

    __logger.info(f"Sent message to {notification.username}")
    if redditor and getattr(redditor, "is_suspended", False):
        return -1
    return 0


def main():
    __logger.info("Starting notification bot")
    with Database() as db:
        while True:
            notification = Notification()
            __redis.blocking_pop(notification)
            user = User(username=notification.username)
            return_value = 0
            if notification.type == Notification.NotificationType.SUBMISSION and user.exists(db):
                return_value = message_user(notification)
                if return_value == 0:
                    user.update_notification_count(db)
            else:
                return_value = message_user(notification)

            if return_value > 0:
                __redis.push(notification)
                time.sleep(return_value)
            elif return_value < 0:
                __logger.info(f"Deleting user {user.username} due to deleted or banned account")
                user.delete(db)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        __logger.critical(f"Unexpected error: {e}")
        raise
