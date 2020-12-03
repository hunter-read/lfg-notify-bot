import praw
import prawcore
import time
import re
import logging
from model import UserRequest, Database
from service import parse_timezone, parse_day, parse_game, timezone_to_gmt, is_nsfw, sort_days


__logger: logging.Logger = logging.getLogger("message_bot")


def read_messages(db: Database, reddit: praw.Reddit):
    for message in reddit.inbox.stream():
        message.mark_read()
        reply = parse_incoming_message(db, message)
        if reply:
            message.reply(reply)
        time.sleep(2)


def parse_incoming_message(db: Database, message: praw.models.Message) -> str:
    user = UserRequest()
    user.username = message.author.name

    full_message = message.subject + message.body
    __logger.info(f"New Message: {message.author.name} - {message.subject}")
    if re.search(r'username mention', message.subject):
        return None

    if re.search(r'(stop|unsubscribe)', full_message, re.IGNORECASE):
        user.delete(db)
        return ("You have successfully stopped notifications from LFG Notify Bot.  \n"
                "If this bot was helpful, please consider making a donation to charity or your GM.")

    elif re.search(r'(bug|issue|error|feature|suggestion)', full_message, re.IGNORECASE):
        return "For error reporting or feature requests, please message u/Perfekthuntr."

    elif re.search(r'(sub(?:scribe)?|notify|lfg(?!\spost))', message.subject, re.IGNORECASE) or parse_game(message.subject):
        game = parse_game(full_message)
        if not game:
            return ("You must include a valid game from the LFG subreddit game tags list https://www.reddit.com/r/lfg/wiki/index/formatting#wiki_game_tags.  \n"
                    "Examples include 5e, CoC, GURPS, or PF1e. Other and Flexible LFG tags are not currently supported.  \n"
                    "&nbsp;  \n"
                    "^^For ^^error ^^reporting, ^^please ^^message ^^u/Perfekthuntr.")

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
                "If you wish to change these settings, reply to this message, or reply **STOP** to end notifications.  \n"
                "&nbsp;  \n"
                "^^For ^^error ^^reporting, ^^please ^^message ^^u/Perfekthuntr.")

    else:
        return ("Unknown message sent. If you wish to subscribe to this bot, please send a new message titled 'Subscribe' with your options in the body of the message.  \n"
                "If you wish to end notifications reply **STOP** to any message, or send a new message titled 'Stop'.  \n"
                "&nbsp;  \n"
                "^^For ^^error ^^reporting, ^^please ^^message ^^u/Perfekthuntr.")


def init_logger(reddit: praw.Reddit) -> None:
    log_file = reddit.config.custom["log_file"]
    log_level = reddit.config.custom["log_level_message_bot"]

    hdlr = logging.FileHandler(log_file) if log_file else logging.StreamHandler()
    str_format = "%(levelname)s:%(name)s:%(asctime)s: %(message)s" if log_file else "%(levelname)s: %(message)s"
    hdlr.setFormatter(logging.Formatter(str_format, "%Y-%m-%d %H:%M:%S"))

    __logger.addHandler(hdlr)
    __logger.setLevel(log_level if log_level else logging.ERROR)


def main():
    reddit: praw.Reddit = praw.Reddit('messages')
    init_logger(reddit)
    __logger.info("Starting incoming message bot")
    database = reddit.config.custom["database"]
    if not database:
        __logger.error("Database location not set. Exiting")
        exit(1)
    with Database(database) as db:
        while True:
            try:
                read_messages(db, reddit)
            except prawcore.exceptions.ServerError as err:
                __logger.error(f"Server Error: {err}")
                time.sleep(10)
            except praw.exceptions.RedditAPIException as err:
                __logger.error(f"API error: {err}")
                time.sleep(10)


if __name__ == "__main__":
    main()
