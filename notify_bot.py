import praw
import prawcore
import time
import logging
from text import *
from model import *


__reddit = praw.Reddit('submissions')
__subreddit = __reddit.subreddit("lfg")


def read_submissions(db):
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
        is_lgbt(submission.title) and flags.append("LGBTQ+")
        is_one_shot(fulltext) and flags.append("One-Shot")
        is_over_18(fulltext) and flags.append("18+")

        if flags:
            logging.info(f"Flags:    {', '.join(flags)}")

        online = is_online(submission.title)
        post.online = int(online)

        timezone = parse_timezone(fulltext)
        if timezone:
            corrected = set([timezone_to_gmt(tz) for tz in timezone])
            output = [f"{tz} ({timezone_to_gmt(tz)})" for tz in timezone]
            logging.info(f"Timezones: {', '.join(output)}")
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
        find_users_and_message(db, user_search, post)

        logging.info("-" * 100)
        logging.info("")


def send_message(user, title, link, time):
    __reddit.redditor(user).message('New LFG Post', f"""Title: {title}  
    Time (best guess): {time if time else 'Unknown'}  
    Link: {__reddit.config.reddit_url}{link}  
    &nbsp;  
    Reply **STOP** to end notifications.
    """)
    time.sleep(2)


def find_users_and_message(db, user_search, post):
    if players_wanted(post.flair) and post.online and post.game:
        users = user_search.find_users(db)
        if users:
            logging.info(f"Users:    {', '.join([i[0] for i in users])}")
            for user in users:
                send_message(user[0], submission.title, submission.permalink, post.time)
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
