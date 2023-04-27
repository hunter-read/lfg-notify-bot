import datetime
import time
import functools
import traceback
from logging import Logger

import praw
import schedule

from model import Database, MessageText, Notification, Post, Redis, User, Spaces
from service import init_logger, find_users_and_queue, init_health_check, set_unhealthy


__NAME: str = "scheduled"
__reddit: praw.Reddit = praw.Reddit(__NAME)
__logger: Logger = init_logger()
__redis: Redis = Redis()


def catch_exceptions():
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except Exception:
                __logger.critical(f"Unexpected error: {traceback.format_exc()}")
                set_unhealthy(__NAME)
                return schedule.CancelJob

        return wrapper

    return catch_exceptions_decorator


@catch_exceptions()
def update_flairless_submission():
    """
    This function will check for any submissions that have been posted in the last 7 minutes and have no flair.
    If a flair has been added, it will update the database and queue the users for notification.
    """
    with Database() as db:
        now = datetime.datetime.utcnow() - datetime.timedelta(minutes=7)
        results = Post.find_post_by_date_created_greater_than_and_no_flair(db, now.strftime("%Y-%m-%d %H:%M:%S"))
        for post in results:
            __logger.info(f"Rechecking flair on post {post.submission_id}")
            submission = __reddit.submission(post.submission_id)
            if submission and getattr(submission, "link_flair_text", None):
                __logger.info(f"Flair added to submission {post.submission_id}")
                post.flair = submission.link_flair_text
                post.update_flair(db)
                find_users_and_queue(db, submission, post)


@catch_exceptions()
def delete_overlimit_users():
    """
    Find all users that have more than 200 notifications queued and unsubscribe them.
    This prevents the bot from sending too many notifications to a user, which could cause the bot to be banned.
    Also, it is unlikely that a user would want to receive more than 200 notifications.
    """
    __logger.info("Running scheduled service to remove overlimit users")
    with Database() as db:
        results = User.find_users_by_notification_count_greater_than(db, 200)
        for user in results:
            __logger.info(f"Unsubscribing user {user.username} due to max notification count")
            notification = Notification(
                username=user.username,
                subject=MessageText.OVERLIMIT_NOTIFICATION_SUBJECT,
                body=MessageText.OVERLIMIT_NOTIFICATION_BODY,
                type=Notification.NotificationType.OVERLIMIT,
            )
            __redis.push(notification)
            user.delete(db)


@catch_exceptions()
def generate_statistics():
    """
    Generate post statistics for the bot and upload them to the Minio server.
    Generates statistics for all time and for the current year.
    """
    year = datetime.datetime.today().year
    # Generate statistics
    with Database() as db:
        data = Post.statistics(db)
        data["generated_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data_year = Post.statistics(db, date=f"{year}-01-01")
        data_year["generated_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Upload statistics to Storage
    spaces: Spaces = Spaces()
    spaces.upload(data, "statistics.json")
    spaces.upload(data_year, f"statistics_{year}.json")

    __logger.info("Generated post statistics")


def main():
    __logger.info("Starting scheduled bot")
    init_health_check(__NAME)
    schedule.every(2).minutes.do(update_flairless_submission)
    schedule.every(4).hours.at(":00").do(delete_overlimit_users)
    schedule.every().day.at("23:59").do(generate_statistics)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
