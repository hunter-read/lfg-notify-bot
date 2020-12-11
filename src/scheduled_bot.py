import time
import schedule
import praw
from logging import Logger
from service.logging_support import init_logger
from model import Database, UserRequest, RedisHandler, Notification, MessageText


__reddit: praw.Reddit = praw.Reddit("scheduled")
__logger: Logger = init_logger("scheduled_bot", __reddit)
__redis: RedisHandler = RedisHandler()


def __init_database() -> Database:
    database = __reddit.config.custom["database"]
    if not database:
        __logger.error("Database location not set. Exiting")
        exit(1)

    return Database(database)


def update_flairless_submission():
    pass


def delete_overlimit_users():
    __logger.info("Running scheduled service to remove overlimit users")
    with __init_database() as db:
        results = UserRequest.find_users_by_notification_count_greater_than(db, 250)
        for user in results:
            __logger.info(f"Unsubscribing user {user.username} due to max notification count")
            notification = Notification(username=user.username, subject=MessageText.OVERLIMIT_NOTIFICATION_SUBJECT, body=MessageText.OVERLIMIT_NOTIFICATION_BODY, type=Notification.NotificationType.OVERLIMIT)
            user.delete(db)
            __redis.push(notification)


def main():
    __logger.info("Starting scheduled bot")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    schedule.every(2).minutes.at(":00").do(update_flairless_submission)
    schedule.every(4).hours.at(":00").do(delete_overlimit_users)
    try:
        main()
    except Exception as e:
        __logger.critical(f"Unexpected error: {e}")
        raise
