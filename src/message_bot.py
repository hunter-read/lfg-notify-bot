from logging import Logger
import os
import time
import re

import praw
import prawcore

from model import Database, MessageText, User, Flair, PlayByPost, Nsfw, Location, Identity, OneShot, AgeLimit, Vtt
from service import init_logger, init_health_check, set_unhealthy
from text import (
    parse_timezone,
    parse_day,
    parse_game,
    game_abbreviation_to_string,
    timezone_to_gmt,
    sort_days,
    find_all_keyword,
    parse_flair,
    parse_message_flags,
)


__NAME: str = "message"
__reddit: praw.Reddit = praw.Reddit(__NAME)
__logger: Logger = init_logger()
__production: bool = os.environ.get("PROFILE") == "production"


def read_messages(db: Database):
    for message in __reddit.inbox.stream():
        reply = parse_incoming_message(db, message)
        if __production ^ message.subject.endswith("devtesting"):
            message.mark_read()
            if reply:
                handle_reply(message, reply)
        else:
            __logger.info(f"Message to {message.author.name}\n{reply}")
        time.sleep(2)


def handle_reply(message: praw.models.Message, reply: str) -> None:
    while True:
        try:
            message.reply(body=reply)
            break
        except praw.exceptions.RedditAPIException as err:
            match = re.search(r"(\d+)\s(minute|millisecond|second)", str(err))
            if "RATELIMIT" in str(err) and match:
                sleep_time = int(match.group(1)) + 1
                if match.group(2) == "minute":
                    sleep_time = sleep_time * 60
                if match.group(2) == "millisecond":
                    sleep_time = 1
                __logger.warning(f"RATELIMIT. Waiting {sleep_time} seconds")
                time.sleep(sleep_time)
            else:
                raise err


def handle_subscribe(db: Database, user: User, message: praw.models.Message) -> str:
    body = message.body

    keywords = find_all_keyword(body)
    if keywords:
        for x in keywords:
            body = body.replace(x, "")

    game = parse_game(message.subject + " " + body)
    if not game:
        return MessageText.MISSING_GAME_REPLY

    user.game = game
    flags = parse_message_flags(body)
    user.online = flags.get("location")
    user.nsfw = flags.get("nsfw")
    user.play_by_post = flags.get("play_by_post")
    user.one_shot = flags.get("one_shot")
    user.lgbtq = flags.get("lgbtq")
    user.age_limit = flags.get("age_limit")
    user.vtt = flags.get("vtt")
    user.match_no_timezone = flags.get("match_no_timezone")
    user.match_no_day = flags.get("match_no_day")
    user.day = parse_day(body)
    user.flair = parse_flair(body) or Flair.DEFAULT.flag

    timezone = parse_timezone(body)
    output = []
    if timezone:
        corrected = set([timezone_to_gmt(tz) for tz in timezone])
        output = [f"{tz} ({timezone_to_gmt(tz)})" for tz in timezone]
        user.timezone = corrected

    flag_string = (
        f"- Including {'Online ' if user.online != Location.OFFLINE.value else ''}"
        f"{'and ' if user.online == Location.ONLINE_AND_OFFLINE.value else ''}"
        f"{'Offline ' if user.online != Location.ONLINE.value else ''}games"
        f"{' only' if user.online != Location.ONLINE_AND_OFFLINE.value else ''}  \n"
    )

    if user.flair and user.flair != Flair.DEFAULT.flag:
        flag_string += f"- Flair: {Flair.flag_to_str(user.flair)}  \n"

    if keywords:
        user.keyword = "|".join([re.escape(keyword) for keyword in keywords])
        flag_string += f"""- Keyword{'s' if len(keywords) > 1 else ''}: "{'" or "'.join(keywords)}"  \n"""

    if user.nsfw != Nsfw.EXCLUDE.value:
        flag_string += f"- {'Only i' if user.nsfw == Nsfw.ONLY else 'I'}nclude NSFW games  \n"
    if user.play_by_post != PlayByPost.INCLUDE.value:
        flag_string += f"- {'Exclude all' if user.play_by_post == PlayByPost.EXCLUDE.value else 'Only include'} Play-by-Post games  \n"
    if user.one_shot != OneShot.INCLUDE.value:
        flag_string += (
            f"- {'Exclude all' if user.one_shot == OneShot.EXCLUDE.value else 'Only include'} One-Shot games  \n"
        )
    if user.lgbtq != Identity.NONE.flag:
        flag_string += f"- Identity Flags: {', '.join(Identity.flag_to_str_array(user.lgbtq))}  \n"
    if user.age_limit != AgeLimit.NONE.value:
        flag_string += f"- Age Limit:  {AgeLimit.tostring(user.age_limit)}  \n"
    if user.vtt != Vtt.NONE.flag:
        flag_string += f"- Virtual Tabletop(s):  {', '.join(Vtt.flag_to_str_array(user.vtt))}  \n"
    if user.match_no_day and user.day:
        flag_string += "- Also including posts with no Day of Week information  \n"
    if user.match_no_timezone and user.timezone:
        flag_string += "- Also including posts with no Timezone information  \n"
    user.save(db)

    return (
        "You have been successfully subscribed to LFG Notify Bot.  \n"
        "&nbsp;  \n"
        "Your current settings are:  \n"
        f"- Game{'s' if len(user.game) > 1 else ''}: {', '.join([game_abbreviation_to_string(game) for game in user.game])}  \n"
        f"- Timezone{'s' if output and len(output) > 1 else ''}: {', '.join(output) if output else 'None Input'}  \n"
        f"- Day{'s' if user.day and len(user.day) > 1 else ''} of the week: {', '.join(sort_days(user.day)) if user.day else 'None Input'}  \n"
        f"{flag_string}"
        "&nbsp;  \n"
        "If you wish to change these settings, reply to this message (include all settings, not just your updates), or reply **STOP** to end notifications.  \n"
        "&nbsp;  \n"
        "^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/user/Perfekthuntr)"
    )


def parse_incoming_message(db: Database, message: praw.models.Message) -> str:
    user = User()

    if not message.author or message.author.name == "reddit" or "Data" in message.subject:
        return None

    user.username = message.author.name

    full_message = message.subject + " " + message.body
    __logger.info(f"New Message: {message.author.name} - {message.subject}")
    if message.was_comment:
        if "comment reply" in message.subject or "post reply" in message.subject:
            return None
        return MessageText.COMMENT_REPLY

    if re.search(r"(stop|unsubscribe)", full_message, re.IGNORECASE):
        user.delete(db)
        return MessageText.UNSUBSCRIBE_REPLY

    elif re.search(r"(bug|issue|error|feature|suggestion)", full_message, re.IGNORECASE):
        return MessageText.ERROR_REPLY

    elif (
        re.search(r"(sub(?:scribe)?|notify|lfg(?!\spost))", message.subject, re.IGNORECASE)
        or parse_game(message.subject)
        or message.subject.endswith("devtesting")
    ):
        return handle_subscribe(db, user, message)

    else:
        return MessageText.UNKNOWN_MESSAGE_REPLY


def main():
    __logger.info("Starting incoming message bot")
    init_health_check(__NAME)
    with Database() as db:
        while True:
            try:
                read_messages(db)
            except prawcore.exceptions.Forbidden as err:
                __logger.error(f"Error sending reply: {err}")
            except prawcore.exceptions.NotFound as err:
                __logger.error(f"Not Found 404 error: {err}")
                time.sleep(30)
            except prawcore.exceptions.ServerError as err:
                __logger.error(f"Server Error: {err}")
                time.sleep(10)
            except praw.exceptions.RedditAPIException as err:
                __logger.error(f"API error: {err}")
                time.sleep(10)
            except prawcore.exceptions.RequestException as err:
                __logger.error(f"Request error: {err}")
                time.sleep(60)
            except prawcore.exceptions.ResponseException as err:
                __logger.error(f"Response error: {err}")
                time.sleep(60)
            except Exception as e:
                __logger.critical(f"Unexpected error: {e}")
                set_unhealthy(__NAME)
                time.sleep(60)


if __name__ == "__main__":
    main()
