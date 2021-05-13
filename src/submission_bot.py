from logging import Logger
import time

import praw
import prawcore

from model import Database, Post
from service import init_logger, find_users_and_queue
from text import timezone_to_gmt, parse_timezone, parse_day, parse_game, game_abbreviation_to_string, parse_time, sort_days, parse_location, parse_submission_flags

__reddit: praw.Reddit = praw.Reddit("submission")
__subreddit: praw.models.Subreddit = __reddit.subreddit("lfg")
__logger: Logger = init_logger()


def read_submissions(db: Database):
    for submission in __subreddit.stream.submissions(skip_existing=True):

        post = Post()

        __logger.info("-" * 100)
        parse_submission(submission, post)
        post.save(db)
        users_string = find_users_and_queue(db, submission, post)
        __logger.info(f"Users:    {users_string}")

        __logger.info("-" * 100)
        __logger.info("")


def parse_submission(submission: praw.models.Submission, post: Post):
    fulltext = submission.title + " " + submission.selftext

    __logger.info(f"New Post: {submission.title} ({submission.link_flair_text})")
    __logger.info(f"Link:     {__reddit.config.reddit_url}{submission.permalink}")
    __logger.info(f"Author:   {submission.author.name}")

    post.submission_id = submission.id
    game = parse_game(submission.title)
    post.game = game
    __logger.info(f"Game:     {', '.join(game)}")

    post.flair = submission.link_flair_text
    post.permalink = submission.permalink
    post.nsfw = submission.over_18

    flags = parse_submission_flags(fulltext)
    post.play_by_post = flags.get("play_by_post")
    post.one_shot = flags.get("one_shot")
    post.lgbtq = flags.get("lgbtq")
    post.age_limit = flags.get("age_limit")
    post.vtt = flags.get("vtt")

    post.online = parse_location(submission.title)

    timezone = parse_timezone(fulltext)
    if timezone:
        corrected = set([timezone_to_gmt(tz) for tz in timezone])
        output = [f"{tz} ({timezone_to_gmt(tz)})" for tz in timezone]
        __logger.info(f"Timezone: {', '.join(output)}")
        post.timezone = corrected

    days = parse_day(fulltext)
    if days:
        __logger.info(f"Days:     {', '.join(sort_days(days))}")
        post.day = days

    start_time, end_time = parse_time(fulltext)
    if start_time:
        post.time = f"{start_time} - {end_time}" if end_time else start_time
        __logger.info(f"Time:     {post.time}")

    __logger.info(f"Flags:    {', '.join(post.flags_as_string_list())}")


def main():
    __logger.info("Starting submission bot")
    with Database() as db:
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
