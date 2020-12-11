from praw.models import Submission

from model import Database, MessageText, Notification, Post, Redis, User
from text import players_wanted, sort_days


def __build_user_search(post: Post) -> User:
    user_search = User()
    user_search.game = post.game
    user_search.timezone = post.timezone
    user_search.day = post.day
    if post.nsfw:
        user_search.nsfw = 1
    return user_search


def find_users_and_queue(db: Database, submission: Submission, post: Post) -> str:
    redis = Redis()

    if not (players_wanted(post.flair) and post.online and post.game):
        return "Invalid match"

    user_search = __build_user_search(post)
    users = user_search.find_users(db)
    if not users:
        return None

    if submission.author.name in users:
        users.remove(submission.author.name)

    if post.nsfw:
        post.flag.append("NSFW")

    notification = Notification()
    notification.subject = MessageText.SUBMISSION_NOTIFICATION_SUBJECT
    notification.body = (f"Title: {submission.title}  \n"
                         f"Timezone(s): {', '.join(post.timezone) if post.timezone else 'Unknown'}  \n"
                         f"Day(s): {', '.join(sort_days(post.day)) if post.day else 'Unknown'}  \n"
                         f"Time: {post.time if post.time else 'Unknown'}  \n"
                         f"Notes: {', '.join(post.flag) if post.flag else 'None'}  \n"
                         f"Link: https://www.reddit.com{post.permalink}  \n"
                         f"{MessageText.SUBMISSION_NOTIFICATION_BODY}")
    notification.type = Notification.NotificationType.SUBMISSION

    for user in users:
        notification.username = user
        redis.append(notification)

    return ', '.join(users)
