import praw
import prawcore
import time
import re
import time_parser
from lfg_database import Database,Post,UserRequest
import logging

__reddit = praw.Reddit('submissions')
__subreddit = __reddit.subreddit("lfg")

__game_regex = re.compile(r"(CoC|3.5|[2-5]e|PF[1-2]e|BitD|BRP|CofD|Cyberpunk|DLC|DLR|DCC|DW|ODND|ADND|BX|DND2e|Earthdawn|Fate|Feast|FWS|GURPS|L5R|MCC|MotW|MM3|Numenera|SWADE|SWD|SR[3-6]|Starfinder|SWRPG|SWN|40K|WoD)", flags=re.IGNORECASE)
__day_regex = re.compile(r"((?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)(?:day))", flags=re.IGNORECASE)
__tz_regex = re.compile(r"[^a-zA-Z](?P<timezone>(GMT|UTC)([+-][0-1]?[0-9]:?[0-5]?[0-9]?)?|ADT|AKDT|AKST|AST|CDT|CST|CT|EDT|EGST|EGT|EST|ET|HDT|HST|MDT|MST|MT|PDT|PST|PT|BST|CEST|CET|EEST|EET|WEST|WET|ACDT|ACST|ACT|AEDT|AEST|AET|AWDT|AWST)[^a-zA-Z]", flags=re.IGNORECASE)
__time_regex = re.compile(r"(?P<time>(([0-9]|[0-1][0-9])(:?[0-5][0-9])?\s*-?\s*(([0-9]|[0-1][0-9])(:?[0-5][0-9])?)?\s*(am|pm))|(?<!(#|/|\d))[0-2][0-9][0-5][0-9]\s*-?\s*([0-2][0-9][0-5][0-9])?)", flags=re.IGNORECASE)

def read_submissions(db):
    for submission in __subreddit.stream.submissions(skip_existing=True):
        if submission.link_flair_text is None:
            continue

        game = re.search(__game_regex, submission.title)
        if game is None:
            continue

        post = Post()
        user_search = UserRequest()
        fulltext = submission.title + submission.selftext

        logging.info("-" * 100)
        logging.info(f"New Post: {submission.title} ({submission.link_flair_text})")
        logging.info(f"Link:     https://www.reddit.com{submission.permalink}")

        
        game = game.group(0).upper()
        post.game = game
        user_search.game = game

        post.permalink = submission.permalink
        post.nsfw = int(submission.is_over_18)

        timezone = re.search(__tz_regex, fulltext)
        if timezone:
            timezone = timezone.group('timezone')
            corrected = time_parser.correct_timezone(timezone)
            logging.info(f"Timezone: {timezone.upper()} ({corrected})")
            post.timezone = corrected
            user_search.timezone = corrected


        days = re.findall(__day_regex, fulltext)
        if days:
            days = set([day.lower().capitalize() for day in days])
            logging.info(f"Days:     {','.join(days)}")
            post.days = days
            user_search.day_of_week = days

        
        times = re.search(__time_regex, fulltext)
        if times is not None:
            time = times.group('time')
            mil_time = time_parser.to_military_time(time)
            logging.info(f"Time:     {time}")
            post.time = mil_time if mil_time else time

        post.save(db)

        if re.search(r"(Player\(s\)\swanted)", submission.link_flair_text, re.IGNORECASE) and re.search(r"(online)", submission.title, re.IGNORECASE) and game is not None:  

            users = user_search.find_users(db)
            logging.info(f"Users:    {[i[0] for i in users]}")
            for user in users:
                send_message(user[0], submission.title, submission.permalink, times.group('time'))
            
        logging.info("-" * 100)
        logging.info("")


def send_message(user, title, link, time):
    __reddit.redditor(user).message('New LFG Post', f"""Title: {title}  
    Start Time (best guess): {time if time else 'Unknown'}  
    Link: https://reddit.com{link}  
    &nbsp;  
    Reply **STOP** to end notifications.
    """)
    time.sleep(2)


def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    with Database() as db: 
        while True:
            try: 
                read_submissions(db)
            except prawcore.exceptions.ServerError as err:
                logging.error(f"Server Error: {err}")
                time.sleep(360)
            except praw.exceptions.RedditAPIException as err:
                logging.error(f"API error: {err}")
                time.sleep(120)


if __name__ == "__main__":
    main()