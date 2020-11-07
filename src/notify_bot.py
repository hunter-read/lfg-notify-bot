import praw
import prawcore
import time
import logging
import typing
from text import timezone_to_gmt, parse_timezone, parse_day, parse_game, parse_time, players_wanted, is_online, is_lgbt, is_one_shot, age_limit
from model import Database, UserRequest, Post


__reddit = praw.Reddit('submissions')
__subreddit = __reddit.subreddit("lfg")


def read_submissions(db: Database):
    for submission in __subreddit.stream.submissions(skip_existing=True):
        if submission.link_flair_text is None:
            logging.warning(f"Found Post with no flair: {__reddit.config.reddit_url}{submission.permalink}")
            continue

        game = parse_game(submission.title)
        if not game:
            continue

        post = Post()
        user_search = UserRequest()
        fulltext = submission.title + submission.selftext

        logging.info("-" * 100)
        logging.info(f"New Post: {submission.title} ({submission.link_flair_text})")
        logging.info(f"Link:     {__reddit.config.reddit_url}{submission.permalink}")

        post.game = game
        user_search.game = game
        logging.info(f"Game:     {', '.join(game)}")

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
            logging.info(f"Flags:    {', '.join(flags)}")

        online = is_online(submission.title)
        post.online = int(online)

        timezone = parse_timezone(fulltext)
        if timezone:
            corrected = set([timezone_to_gmt(tz) for tz in timezone])
            output = [f"{tz} ({timezone_to_gmt(tz)})" for tz in timezone]
            logging.info(f"Timezone: {', '.join(output)}")
            post.timezone = corrected
            user_search.timezone = corrected

        days = parse_day(fulltext)
        if days:
            logging.info(f"Days:     {','.join([day.capitalize() for day in days])}")
            post.days = days
            user_search.days = days

        start_time, end_time = parse_time(fulltext)
        if start_time:
            post.time = f"{start_time} - {end_time}" if end_time else start_time
            logging.info(f"Time:     {post.time}")

        post.save(db)
        if players_wanted(post.flair) and post.online and post.game:
            find_users_and_message(db, user_search, submission.title, post, flags)

        logging.info("-" * 100)
        logging.info("")


def find_users_and_message(db: Database, user_search: UserRequest, title: str, post: Post, flags: typing.List[str]) -> None:
    users = user_search.find_users(db)
    if users:
        logging.info(f"Users:    {', '.join([i[0] for i in users])}")
        for user in users:
            __reddit.redditor(user[0]).message('New LFG Post matching your criteria',
                                               (f"Title: {title}  \n"
                                                f"Days: {','.join([day.capitalize() for day in post.days]) if post.days else 'Unknown'}  \n"
                                                f"Time: {post.times if post.times else 'Unknown'}  \n"
                                                f"Notes: {', '.join(flags) if flags else 'None'}  \n"
                                                f"Link: {__reddit.config.reddit_url}{post.permalink}  \n"
                                                "&nbsp;  \n"
                                                "Reply **STOP** to end notifications."))
            time.sleep(2)
    else:
        logging.info("Users:    None")


def main():
    log_file = __reddit.config.custom["log_file"]
    log_level = int(__reddit.config.custom["log_level_notify_bot"])
    logging.basicConfig(format='%(levelname)s:%(message)s', level=log_level, filename=log_file)

    database = __reddit.config.custom["database"]
    if not database:
        logging.error("Database location not set. Exiting")
        exit(1)

    with Database(database) as db:
        while True:
            try:
                read_submissions(db)
            except prawcore.exceptions.ServerError as err:
                logging.error(f"Server Error: {err}")
                time.sleep(10)
            except praw.exceptions.RedditAPIException as err:
                logging.error(f"API error: {err}")
                time.sleep(10)


if __name__ == "__main__":
    main()
