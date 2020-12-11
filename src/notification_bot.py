import praw
import prawcore
import time
import re
import pprint
from logging import Logger
from service import init_logger
from model import Database, UserRequest, RedisHandler, Notification

__reddit: praw.Reddit = praw.Reddit("notification")
__logger: Logger = init_logger("notification_bot", __reddit)
__redis: RedisHandler = RedisHandler()


def message_user(notification: Notification) -> int:
    if __reddit.config.custom["environment"] != "production":
        __logger.info(f"Recieved message for {notification.username}")
        return 0

    try:
        redditor = __reddit.redditor(notification.username)
        redditor.message(notification.subject, notification.body)

    except prawcore.exceptions.Forbidden as err:
        __logger.error(f"Error sending message to {notification.username}: {err}")
        return 0

    except praw.exceptions.RedditAPIException as err:
        match = re.search(r"(\d+)\s(minute|millisecond|second)", str(err))

        if "RATELIMIT" in str(err) and match:
            sleep_time = int(match.group(1)) + 1
            if match.group(2) == "minute":
                sleep_time = (sleep_time * 60)
            if match.group(2) == "millisecond":
                sleep_time = 1
            __logger.warning(f"RATELIMIT. Waiting {sleep_time} seconds")
            return sleep_time
        else:
            __logger.error(f"Api Error: {err}")
            return 30

    except prawcore.exceptions.ServerError as err:
        __logger.error(f"Server Error: {err}")
        return 30

    __logger.info(f"Sent message to {notification.username}")
    if redditor and getattr(redditor, "is_suspended", False):
        return -1
    return 0


def main():
    __logger.info("Starting notification bot")
    database = __reddit.config.custom["database"]
    if not database:
        __logger.error("Database location not set. Exiting")
        exit(1)

    with Database(database) as db:
        while True:
            notification = __redis.blocking_pop(Notification)
            user = UserRequest(username=notification.username)
            return_value = 0
            if notification.type == Notification.NotificationType.SUBMISSION and not user.exists(db):
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
