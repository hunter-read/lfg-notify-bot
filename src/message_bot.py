from logging import Logger
import os
import time
import re

import praw
import prawcore

from model import Database, MessageText, User, Flair, PlayByPost, Nsfw, Location, Lgbtq, OneShot, AgeLimit, Vtt
from service import init_logger
from text import parse_timezone, parse_day, parse_game, timezone_to_gmt, sort_days, find_all_keyword, parse_flair, parse_message_flags


__reddit: praw.Reddit = praw.Reddit("message")
__logger: Logger = init_logger()
__production: bool = os.environ.get('PROFILE') == "production"


def read_messages(db: Database):
    for message in __reddit.inbox.stream():
        reply = parse_incoming_message(db, message)
        if __production ^ message.subject.endswith("devtesting"):
            message.mark_read()
            if reply:
                message.reply(reply)
        else:
            __logger.info(f"Message to {message.author.name}\n{reply}")
        time.sleep(2)


def handle_subscribe(db: Database, user: User, message: praw.models.Message) -> str:
    game = parse_game(message.subject + ' ' + message.body)
    if not game:
        return MessageText.MISSING_GAME_REPLY

    user.game = game
    flags = parse_message_flags(message.body)
    user.online = flags.get("location")
    user.nsfw = flags.get("nsfw")
    user.play_by_post = flags.get("play_by_post")
    user.one_shot = flags.get("one_shot")
    user.lgbtq = flags.get("lgbtq")
    user.age_limit = flags.get("age_limit")
    user.vtt = flags.get("vtt")
    user.day = parse_day(message.body)
    user.flair = parse_flair(message.body) or Flair.DEFAULT.flag

    timezone = parse_timezone(message.body)
    output = []
    if timezone:
        corrected = set([timezone_to_gmt(tz) for tz in timezone])
        output = [f"{tz} ({timezone_to_gmt(tz)})" for tz in timezone]
        user.timezone = corrected

    flag_string = f"- Including {'Online ' if user.online != Location.OFFLINE else ''}{'and ' if user.online == Location.ONLINE_AND_OFFLINE else ''}{'Offline ' if user.online != Location.ONLINE else ''}games{' only' if user.online != Location.ONLINE_AND_OFFLINE else ''}  \n"

    if user.flair and user.flair != Flair.DEFAULT.flag:
        flag_string += f"- Flair: {Flair.flag_to_str(user.flair)}  \n"

    keywords = find_all_keyword(message.body)
    if keywords:
        user.keyword = '|'.join([re.escape(keyword) for keyword in keywords])
        flag_string += f"""- Keyword{'s' if len(keywords) > 1 else ''}: "{'" or "'.join(keywords)}"  \n"""

    if user.nsfw != Nsfw.EXCLUDE:
        flag_string += f"- Include {'only ' if user.nsfw == Nsfw.ONLY else ''}NSFW games  \n"
    if user.play_by_post != PlayByPost.INCLUDE:
        flag_string += f"- {'Exclude' if user.play_by_post == PlayByPost.EXCLUDE else 'Include only'} Play-by-Post games  \n"
    if user.one_shot != OneShot.INCLUDE:
        flag_string += f"- {'Exclude' if user.one_shot == OneShot.EXCLUDE else 'Include only'} One-Shot games  \n"
    if user.lgbtq != Lgbtq.ONLY:
        flag_string += "- Only including LGBTQ+ labeled games  \n"
    if user.age_limit != AgeLimit.NONE:
        flag_string += f"- Age Limit:  {AgeLimit.tostring(user.age_limit)}  \n"
    if user.vtt != Vtt.NONE:
        flag_string += f"- Virtual Tabletop:  {', '.join(Vtt.flag_to_str_array(user.vtt))}  \n"

    user.save(db)

    return ("You have been successfully subscribed to LFG Notify Bot.  \n"
            "&nbsp;  \n"
            "Your current settings are:  \n"
            f"- Game{'s' if len(user.game) > 1 else ''}: {', '.join(user.game)}  \n"
            f"- Timezone{'s' if output and len(output) > 1 else ''}: {', '.join(output) if output else 'None Input'}  \n"
            f"- Day{'s' if user.day and len(user.day) > 1 else ''} of the week: {', '.join(sort_days(user.day)) if user.day else 'None Input'}  \n"
            f"{flag_string}"
            "&nbsp;  \n"
            "If you wish to change these settings, reply to this message (include all settings, not just your updates), or reply **STOP** to end notifications.  \n"
            "&nbsp;  \n"
            "^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/user/Perfekthuntr)")


def parse_incoming_message(db: Database, message: praw.models.Message) -> str:
    user = User()

    if not message.author or message.author.name == 'reddit' or "Data" in message.subject:
        return None

    user.username = message.author.name

    full_message = message.subject + ' ' + message.body
    __logger.info(f"New Message: {message.author.name} - {message.subject}")
    if message.was_comment:
        if "comment reply" in message.subject:
            return None
        return MessageText.COMMENT_REPLY

    if re.search(r'(stop|unsubscribe)', full_message, re.IGNORECASE):
        user.delete(db)
        return MessageText.UNSUBSCRIBE_REPLY

    elif re.search(r'(bug|issue|error|feature|suggestion)', full_message, re.IGNORECASE):
        return MessageText.ERROR_REPLY

    elif re.search(r'(sub(?:scribe)?|notify|lfg(?!\spost))', message.subject, re.IGNORECASE) or parse_game(message.subject) or message.subject.endswith("devtesting"):
        return handle_subscribe(db, user, message)

    else:
        return MessageText.UNKNOWN_MESSAGE_REPLY


def main():
    __logger.info("Starting incoming message bot")
    with Database() as db:
        while True:
            try:
                read_messages(db)
            except prawcore.exceptions.Forbidden as err:
                __logger.error(f"Error sending reply: {err}")
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
