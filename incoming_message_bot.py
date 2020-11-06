import praw
import prawcore
import time
import re
import logging
from model import UserRequest, Database
from text import parse_timezone, parse_day, parse_game, timezone_to_gmt, is_nsfw


__reddit = praw.Reddit('messages')


def read_messages(db: Database):
    for message in __reddit.inbox.stream():

        user = UserRequest()
        user.username = message.author.name

        message.mark_read()
        logging.info(f"New Message: {message.author.name} - {message.subject}")

        if re.search(r'stop', message.subject + message.body, re.IGNORECASE):
            user.delete(db)
            message.reply(body=("You have successfully stopped notifications from LFG Notify Bot.  \n"
                                "If this bot was helpful, please consider making a donation to charity or your GM."))
            time.sleep(2)

        elif re.search(r'subscribe', message.subject, re.IGNORECASE):
            game = parse_game(message.body)
            if not game:
                message.reply(body=("You must include a valid game from the LFG subreddit game tags list https://www.reddit.com/r/lfg/wiki/index/formatting#wiki_game_tags. Other and Flexible LFG tags are not currently supported.  \n"
                                    "&nbsp;  \n"
                                    "^^For ^^error ^^reporting, ^^please ^^message ^^u/Perfekthuntr."))
                continue

            user.game = game
            user.days = parse_day(message.body)

            timezone = parse_timezone(message.body)
            if timezone:
                corrected = set([timezone_to_gmt(tz) for tz in timezone])
                output = [f"{tz} ({timezone_to_gmt(tz)})" for tz in timezone]
                logging.info(f"Timezones: {', '.join(output)})")
                user.timezone = corrected

            user.nsfw = is_nsfw(message.body)

            user.save(db)

            message.reply(body=(f"You have been successfully subscribed to LFG Notify Bot.  \n"
                                "&nbsp;  \n"
                                "Your current settings are:  \n"
                                f"- Timezone(s): {', '.join(output)}  \n"
                                f"- Game(s): {', '.join(user.game)}  \n"
                                f"- Day(s) of the week: {', '.join([day.capitalize() for day in user.days])}  \n"
                                f"- Include NSFW: {'No' if user.nsfw == 0 else 'Yes'}  \n"
                                "&nbsp;  \n"
                                "If you wish to change these settings, reply to this message, or reply **STOP** to end notifications.  \n"
                                "&nbsp;  \n"
                                "^^For ^^error ^^reporting, ^^please ^^message ^^u/Perfekthuntr."))
            time.sleep(2)


def main():
    __backoff = 5
    log_file = __reddit.config.custom["log_file"]
    log_level = int(__reddit.config.custom["log_level_message_bot"])
    logging.basicConfig(format='%(levelname)s:%(asctime)s:%(message)s', level=log_level, filename=log_file, datefmt='%Y-%m-%d %H:%M:%S')

    database = __reddit.config.custom["database"]
    if not database:
        logging.error("Database location not set. Exiting")
        exit(1)
    with Database(database) as db:
        while True:
            try:
                read_messages(db)
            except prawcore.exceptions.ServerError as err:
                logging.error(f"Server Error: {err}")
                time.sleep(__backoff)
                __backoff *= 2
            except praw.exceptions.RedditAPIException as err:
                logging.error(f"API error: {err}")
                time.sleep(__backoff)
                __backoff *= 2


if __name__ == "__main__":
    main()
