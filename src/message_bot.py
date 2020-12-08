import praw
import prawcore
import time
import re
import model.constants as constants
from logging import Logger
from model import UserRequest, Database
from service import parse_timezone, parse_day, parse_game, timezone_to_gmt, is_nsfw, sort_days, init_logger

__reddit: praw.Reddit = praw.Reddit("message")
__logger: Logger = init_logger("message_bot", __reddit)


def read_messages(db: Database):
    for message in __reddit.inbox.stream():
        reply = parse_incoming_message(db, message)
        if __reddit.config.custom["environment"] == "production":
            message.mark_read()
            if reply:
                message.reply(reply)
        time.sleep(2)


def parse_incoming_message(db: Database, message: praw.models.Message) -> str:
    user = UserRequest()
    user.username = message.author.name

    full_message = message.subject + message.body
    __logger.info(f"New Message: {message.author.name} - {message.subject}")
    if message.was_comment:
        return constants.COMMENT_REPLY

    if re.search(r'reddit|I would like to join|username mention', message.subject):
        return None

    if re.search(r'(stop|unsubscribe)', full_message, re.IGNORECASE):
        user.delete(db)
        return constants.UNSUBSCRIBE_REPLY

    elif re.search(r'(bug|issue|error|feature|suggestion)', full_message, re.IGNORECASE):
        return constants.ERROR_REPLY

    elif re.search(r'(sub(?:scribe)?|notify|lfg(?!\spost))', message.subject, re.IGNORECASE) or parse_game(message.subject):
        game = parse_game(full_message)
        if not game:
            return constants.MISSING_GAME_REPLY

        user.game = game
        user.nsfw = is_nsfw(message.body)
        user.days = parse_day(message.body)
        timezone = parse_timezone(message.body)
        output = []
        if timezone:
            corrected = set([timezone_to_gmt(tz) for tz in timezone])
            output = [f"{tz} ({timezone_to_gmt(tz)})" for tz in timezone]
            user.timezone = corrected

        user.save(db)

        return (f"You have been successfully subscribed to LFG Notify Bot.  \n"
                "&nbsp;  \n"
                "Your current settings are:  \n"
                f"- Game(s): {', '.join(user.game)}  \n"
                f"- Timezone(s): {', '.join(output) if output else 'None Input'}  \n"
                f"- Day(s) of the week: {', '.join(sort_days(user.days)) if user.days else 'None Input'}  \n"
                f"- Include NSFW: {'No' if user.nsfw == 0 else 'Yes'}  \n"
                "&nbsp;  \n"
                "If you wish to change these settings, reply to this message (include all settings, not just your updates), or reply **STOP** to end notifications.  \n"
                "&nbsp;  \n"
                "^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/user/Perfekthuntr)")

    else:
        return constants.UNKNOWN_MESSAGE_REPLY


def main():
    __logger.info("Starting incoming message bot")
    database = __reddit.config.custom["database"]
    if not database:
        __logger.error("Database location not set. Exiting")
        exit(1)
    with Database(database) as db:
        while True:
            try:
                read_messages(db)
            except prawcore.exceptions.ServerError as err:
                __logger.error(f"Server Error: {err}")
                time.sleep(10)
            except praw.exceptions.RedditAPIException as err:
                __logger.error(f"API error: {err}")
                time.sleep(10)


if __name__ == "__main__":
    main()
