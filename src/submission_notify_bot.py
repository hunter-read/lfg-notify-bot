import praw
import prawcore
import time
import logging
import typing
from service import timezone_to_gmt, parse_timezone, parse_day, parse_game, parse_time, players_wanted, is_online, is_lgbt, is_one_shot, age_limit, sort_days
from model import Database, UserRequest, Post


__reddit: praw.Reddit = praw.Reddit('submissions')
__subreddit: praw.models.Subreddit = __reddit.subreddit("lfg")
__logger: logging.Logger = logging.getLogger('notify_bot')


def read_submissions(db: Database):
    for submission in __subreddit.stream.submissions(skip_existing=True):
        if submission.link_flair_text is None:
            __logger.warning(f"Found Post with no flair: {__reddit.config.reddit_url}{submission.permalink}")
            continue

        game = parse_game(submission.title)
        if not game:
            continue

        post = Post()
        user_search = UserRequest()
        fulltext = submission.title + submission.selftext

        __logger.info("-" * 100)
        __logger.info(f"New Post: {submission.title} ({submission.link_flair_text})")
        __logger.info(f"Link:     {__reddit.config.reddit_url}{submission.permalink}")

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

        post.save(db)
        if players_wanted(post.flair) and post.online and post.game:
            find_users_and_message(db, user_search, submission.title, post, flags)

        __logger.info("-" * 100)
        __logger.info("")


def find_users_and_message(db: Database, user_search: UserRequest, title: str, post: Post, flags: typing.List[str]) -> None:
    users = user_search.find_users(db)
    if users:
        __logger.info(f"Users:    {', '.join([i[0] for i in users])}")
        for user in users:
            __reddit.redditor(user[0]).message('New LFG post matching your criteria',
                                               (f"Title: {title}  \n"
                                                f"Timezone(s): {', '.join(post.timezone) if post.timezone else 'Unknown'}  \n"
                                                f"Day(s): {', '.join(sort_days(post.days)) if post.days else 'Unknown'}  \n"
                                                f"Time: {post.time if post.time else 'Unknown'}  \n"
                                                f"Notes: {', '.join(flags) if flags else 'None'}  \n"
                                                f"Link: {__reddit.config.reddit_url}{post.permalink}  \n"
                                                "&nbsp;  \n"
                                                "Reply **STOP** to end notifications.  \n"
                                                "&nbsp;  \n"
                                                "^Reminder ^that ^all ^information ^provided ^is ^a ^best ^guess, ^and ^you ^should ^read ^the ^post ^linked ^above"))
            time.sleep(2)
    else:
        __logger.info("Users:    None")


def init_logger() -> None:
    log_file = __reddit.config.custom["log_file"]
    log_level = __reddit.config.custom["log_level_notify_bot"]

    hdlr = logging.FileHandler(log_file) if log_file else logging.StreamHandler()
    str_format = "%(levelname)s:%(name)s: %(message)s" if log_file else "%(levelname)s: %(message)s"
    hdlr.setFormatter(logging.Formatter(str_format))

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
                time.sleep(10)


if __name__ == "__main__":
    main()
