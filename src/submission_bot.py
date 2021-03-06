from logging import Logger
import time

import praw
import prawcore

from model import Database, Post
from service import init_logger, find_users_and_queue
from text import timezone_to_gmt, parse_timezone, parse_day, parse_game, parse_time, is_online, is_offline, is_lgbt, is_one_shot, age_limit, using_vtt, sort_days, is_play_by_post

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
    post.nsfw = int(submission.over_18)

    is_lgbt(fulltext) and post.flag.append("LGBTQ+")
    is_one_shot(fulltext) and post.flag.append("One-Shot")
    is_play_by_post(fulltext) and post.flag.append("Play-by-Post")
    vtt = using_vtt(fulltext)
    vtt and post.flag.append(vtt)
    age_limit_text = age_limit(fulltext)
    if age_limit_text:
        post.flag.append(age_limit_text)

    if post.flag:
        __logger.info(f"Flags:    {', '.join(post.flag)}")

    post.online = 0
    online = is_online(submission.title)
    offline = is_offline(submission.title)
    if online or offline:
        if online:
            post.online += 1
        if offline:
            post.online -= 1
    else:
        post.online = -9

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
