from logging import Logger
import datetime
import json
import time

import praw
import schedule
from io import BytesIO
from minio import Minio

from model import Database, MessageText, Notification, Post, Redis, User
from service import init_logger, find_users_and_queue


__reddit: praw.Reddit = praw.Reddit("scheduled")
__logger: Logger = init_logger()
__redis: Redis = Redis()


def update_flairless_submission():
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


def delete_overlimit_users():
    __logger.info("Running scheduled service to remove overlimit users")
    with Database() as db:
        results = User.find_users_by_notification_count_greater_than(db, 200)
        for user in results:
            __logger.info(f"Unsubscribing user {user.username} due to max notification count")
            notification = Notification(username=user.username, subject=MessageText.OVERLIMIT_NOTIFICATION_SUBJECT, body=MessageText.OVERLIMIT_NOTIFICATION_BODY, type=Notification.NotificationType.OVERLIMIT)
            __redis.push(notification)
            user.delete(db)


def generate_statistics():
    year = datetime.datetime.today().year
    with Database() as db:
        data = Post.statistics(db)
        data["generated_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")

        data_year = Post.statistics(db, date=f"{year}-01-01")
        data_year["generated_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        
    client = Minio(__reddit.config.custom["statistics_endpoint"], 
                   __reddit.config.custom["minio_access_key"], 
                   __reddit.config.custom["minio_secret_key"], 
                   secure=True)
    
    byte = json.dumps(data).encode("utf-8")
    client.put_object(__reddit.config.custom["bucket_name"], "statistics.json", byte, len(byte), content_type="application/json")
    
    byte_year = json.dumps(data_year).encode("utf-8")
    client.put_object("lfg-notify-bot", f"statistics_{year}.json", byte_year, len(byte_year), content_type="application/json")    
    
    __logger.info("Generated post statistics")

def main():
    __logger.info("Starting scheduled bot")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    schedule.every(2).minutes.do(update_flairless_submission)
    schedule.every(4).hours.at(":00").do(delete_overlimit_users)
    schedule.every().day.at("23:59").do(generate_statistics)
    try:
        main()
    except Exception as e:
        __logger.critical(f"Unexpected error: {e}")
        raise
