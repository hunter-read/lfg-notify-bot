import praw
import prawcore
import time
import typing
from logging import Logger
from service import timezone_to_gmt, parse_timezone, parse_day, parse_game, parse_time, players_wanted, is_online, is_lgbt, is_one_shot, age_limit, sort_days, using_vtt, init_logger
from model import Database, Post, UserRequest, RedisHandler, Notification, MessageText

__reddit: praw.Reddit = praw.Reddit("submission")
__subreddit: praw.models.Subreddit = __reddit.subreddit("lfg")
__logger: Logger = init_logger("submission_bot", __reddit)
__redis: RedisHandler = RedisHandler()


def read_submissions(db: Database):
    for submission in __subreddit.stream.submissions(skip_existing=True):

        post = Post()
        user_search = UserRequest()
        flags = []

        __logger.info("-" * 100)
        parse_submission(submission, post, user_search, flags)

        if post.flair:
            post.save(db)

        if players_wanted(post.flair) and post.online and post.game:
            find_users_and_queue(db, user_search, submission, post, flags)

        __logger.info("-" * 100)
        __logger.info("")


def find_users_and_queue(db: Database, user_search: UserRequest, submission: praw.models.Submission, post: Post, flags: typing.List[str]) -> None:
    users = user_search.find_users(db)
    if not users:
        __logger.info("Users:    None")
        return

    if submission.author.name in users:
        users.remove(submission.author.name)

    __logger.info(f"Users:    {', '.join(users)}")

    notification = Notification()
    notification.subject = MessageText.SUBMISSION_NOTIFICATION_SUBJECT
    notification.body = (f"Title: {submission.title}  \n"
                         f"Timezone(s): {', '.join(post.timezone) if post.timezone else 'Unknown'}  \n"
                         f"Day(s): {', '.join(sort_days(post.days)) if post.days else 'Unknown'}  \n"
                         f"Time: {post.time if post.time else 'Unknown'}  \n"
                         f"Notes: {', '.join(flags) if flags else 'None'}  \n"
                         f"Link: {__reddit.config.reddit_url}{post.permalink}  \n"
                         f"{MessageText.SUBMISSION_NOTIFICATION_BODY}")
    notification.type = Notification.NotificationType.SUBMISSION

    for user in users:
        notification.username = user
        __redis.append(notification)


def parse_submission(submission: praw.models.Submission, post: Post, user_search: UserRequest, flags: typing.List[str]):
    if not submission.link_flair_text:
        __logger.warning(f"Found Post with no flair: {__reddit.config.reddit_url}{submission.permalink}")

    fulltext = submission.title + submission.selftext

    __logger.info(f"New Post: {submission.title} ({submission.link_flair_text})")
    __logger.info(f"Link:     {__reddit.config.reddit_url}{submission.permalink}")
    __logger.info(f"Author:   {submission.author.name}")

    post.submission_id = submission.id
    game = parse_game(submission.title)
    post.game = game
    user_search.game = game
    __logger.info(f"Game:     {', '.join(game)}")

    post.flair = submission.link_flair_text
    post.permalink = submission.permalink
    post.nsfw = int(submission.over_18)

    flags = []
    post.nsfw and flags.append("NSFW")
    is_lgbt(fulltext) and flags.append("LGBTQ+")
    is_one_shot(fulltext) and flags.append("One-Shot")
    vtt = using_vtt(fulltext)
    vtt and flags.append(vtt)
    age_limit_text = age_limit(fulltext)
    if age_limit_text:
        flags.append(age_limit_text)

    if flags:
        __logger.info(f"Flags:    {', '.join(flags)}")

    post.online = is_online(submission.title)

    timezone = parse_timezone(fulltext)
    if timezone:
        corrected = set([timezone_to_gmt(tz) for tz in timezone])
        output = [f"{tz} ({timezone_to_gmt(tz)})" for tz in timezone]
        __logger.info(f"Timezone: {', '.join(output)}")
        post.timezone = corrected
        user_search.timezone = corrected

    days = parse_day(fulltext)
    if days:
        __logger.info(f"Days:     {', '.join(sort_days(days))}")
        post.days = days
        user_search.days = days

    start_time, end_time = parse_time(fulltext)
    if start_time:
        post.time = f"{start_time} - {end_time}" if end_time else start_time
        __logger.info(f"Time:     {post.time}")


def main():
    __logger.info("Starting submission bot")
    database = __reddit.config.custom["database"]
    if not database:
        __logger.error("Database location not set. Exiting")
        exit(1)

    with Database(database) as db:
        while True:
            try:
                read_submissions(db)
            except prawcore.exceptions.ServerError as err:
                __logger.error(f"Server Error: {err}")
                time.sleep(10)
            except praw.exceptions.RedditAPIException as err:
                __logger.error(f"API error: {err}")
                time.sleep(10)
            except Exception as e:
                __logger.critical(f"Unexpected error: {e}")
                raise


if __name__ == "__main__":
    main()
