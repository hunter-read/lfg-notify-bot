import re

from praw.models import Submission

from model import Database, MessageText, Notification, Post, Redis, User, Location
from text import sort_days, parse_flair


def __build_user_search(post: Post) -> User:
    user_search = User()
    user_search.game = post.game
    user_search.timezone = post.timezone
    user_search.day = post.day
    user_search.online = post.online
    user_search.nsfw = int(post.nsfw)
    user_search.play_by_post = int(post.play_by_post)
    user_search.one_shot = int(post.one_shot)
    user_search.lgbtq = int(post.lgbtq)
    user_search.age_limit = post.age_limit
    user_search.vtt = post.vtt

    user_search.flair = parse_flair(post.flair)
    return user_search


def filter_user_list(users: list, submission: Submission) -> list:
    filtered_users = []
    for user in users:
        if user.username == submission.author.name:
            pass
        elif not user.keyword:
            filtered_users.append(user.username)
        elif re.search(rf"{user.keyword}", submission.title + submission.selftext, re.IGNORECASE):
            filtered_users.append(user.username)
    return filtered_users


def find_users_and_queue(db: Database, submission: Submission, post: Post) -> str:
    redis = Redis()

    user_search = __build_user_search(post)

    if not post.flair:
        return "Missing flair"
    if post.online == Location.NONE.value:
        return "Missing online or offline"
    if not post.game:
        return "Missing or invalid game"

    users = user_search.find_users(db)
    if not users:
        return None

    users = filter_user_list(users, submission)

    flags = post.flags_as_string_list()
    notification = Notification()
    notification.subject = MessageText.SUBMISSION_NOTIFICATION_SUBJECT
    notification.body = (
        f"Title: {submission.title}  \n"
        f"Flair: {submission.link_flair_text}  \n"
        f"Timezone(s): {', '.join(post.timezone) if post.timezone else 'Unknown'}  \n"
        f"Day(s): {', '.join(sort_days(post.day)) if post.day else 'Unknown'}  \n"
        f"Time: {post.time if post.time else 'Unknown'}  \n"
        f"Notes: {', '.join(flags) if flags else 'None'}  \n"
        f"Link: https://www.reddit.com{post.permalink}  \n"
        f"{MessageText.SUBMISSION_NOTIFICATION_BODY}"
    )
    notification.type = Notification.NotificationType.SUBMISSION

    for user in users:
        notification.username = user
        redis.append(notification)

    return ", ".join(users)
