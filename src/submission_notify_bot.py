import praw
import prawcore
import time
import logging
import typing
import traceback
import re
from service import timezone_to_gmt, parse_timezone, parse_day, parse_game, parse_time, players_wanted, is_online, is_lgbt, is_one_shot, age_limit, sort_days, using_vtt
from model import Database, UserRequest, Post


__reddit: praw.Reddit = praw.Reddit('submissions')
__subreddit: praw.models.Subreddit = __reddit.subreddit("lfg")
__logger: logging.Logger = logging.getLogger('notify_bot')


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
            find_users_and_message(db, user_search, submission, post, flags)

        __logger.info("-" * 100)
        __logger.info("")


def find_users_and_message(db: Database, user_search: UserRequest, submission: praw.models.Submission, post: Post, flags: typing.List[str]) -> None:
    users = user_search.find_users(db)
    if not users:
        __logger.info("Users:    None")
        return
    users = [user for user in users if user.username != submission.author.name]
    __logger.info(f"Users:    {', '.join([user.username for user in users])}")
    index = 0
    while index < len(users):
        try:
            __reddit.redditor(users[index].username).message(
                'New LFG post matching your criteria',
                (f"Title: {submission.title}  \n"
                    f"Timezone(s): {', '.join(post.timezone) if post.timezone else 'Unknown'}  \n"
                    f"Day(s): {', '.join(sort_days(post.days)) if post.days else 'Unknown'}  \n"
                    f"Time: {post.time if post.time else 'Unknown'}  \n"
                    f"Notes: {', '.join(flags) if flags else 'None'}  \n"
                    f"Link: {__reddit.config.reddit_url}{post.permalink}  \n"
                    "&nbsp;  \n"
                    "Reply **STOP** to end notifications.  \n"
                    "&nbsp;  \n"
                    "^Reminder ^that ^all ^information ^provided ^is ^a ^best ^guess, ^and ^you ^should ^read ^the ^post ^linked ^above"))
        except praw.exceptions.RedditAPIException as err:
            match = re.search(r"(\d+)\s(minute|millisecond|second)", str(err))

            if "RATELIMIT" in str(err) and match:
                sleep_time = int(match.group(1))
                if match.group(2) == "minute":
                    sleep_time = (sleep_time * 60)
                if match.group(2) == "millisecond":
                    sleep_time = 1
                sleep_time += 1
                __logger.warning(f"Rate Limit hit after {index} private messages. Waiting {sleep_time} seconds")
                time.sleep(sleep_time)
            else:
                raise

        except prawcore.exceptions.ServerError as err:
            __logger.error(f"Server Error: {err}")
            time.sleep(10)

        else:
            time.sleep(10)
            users[index].update_notification_count(db)
            index += 1


def parse_submission(submission: praw.models.Submission, post: Post, user_search: UserRequest, flags: typing.List[str]):
    if not submission.link_flair_text:
        __logger.warning(f"Found Post with no flair: {__reddit.config.reddit_url}{submission.permalink}")

    fulltext = submission.title + submission.selftext

    __logger.info(f"New Post: {submission.title} ({submission.link_flair_text})")
    __logger.info(f"Link:     {__reddit.config.reddit_url}{submission.permalink}")
    __logger.info(f"Author:   {submission.author.name}")

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


def init_logger() -> None:
    log_file = __reddit.config.custom["log_file"]
    log_level = __reddit.config.custom["log_level_notify_bot"]

    hdlr = logging.FileHandler(log_file) if log_file else logging.StreamHandler()
    str_format = "%(levelname)s:%(name)s:%(asctime)s: %(message)s" if log_file else "%(levelname)s: %(message)s"
    hdlr.setFormatter(logging.Formatter(str_format, "%Y-%m-%d %H:%M:%S"))

    __logger.addHandler(hdlr)
    __logger.setLevel(log_level if log_level else logging.ERROR)


def main():
    init_logger()
    __logger.info("Starting submission notify bot")
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
                time.sleep(60)
            except Exception as e:
                __logger.error(traceback.format_exc())
                raise e


if __name__ == "__main__":
    main()
