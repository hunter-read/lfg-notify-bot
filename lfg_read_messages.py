import praw
import prawcore
import time
import re
from lfg_database import Database,UserRequest
import time_parser
import logging

reddit = praw.Reddit('messages')

game_regex = re.compile(r"(CoC|3.5|[2-5]e|PF[1-2]e|BitD|BRP|CofD|Cyberpunk|DLC|DLR|DCC|DW|ODND|ADND|BX|DND2e|Earthdawn|Fate|Feast|FWS|GURPS|L5R|MCC|MotW|MM3|Numenera|SWADE|SWD|SR[3-6]|Starfinder|SWRPG|SWN|40K|WoD)", flags=re.IGNORECASE)
day_regex = re.compile(r"((?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)(?:day))", flags=re.IGNORECASE)
tz_regex = re.compile(r"((?:GMT|UTC)(?:[+-][0-1]?[0-9]:?[0-5]?[0-9]?)?|ADT|AKDT|AKST|AST|CDT|CST|EDT|EGST|EGT|EST|HDT|HST|MDT|MST|MT|PDT|PST|BST|CEST|CET|EEST|EET|WEST|WET|ACDT|ACST|ACT|AEDT|AEST|AET|AWDT|AWST)", flags=re.IGNORECASE)

def read_messages(db):
    for message in reddit.inbox.stream():
        
        user = UserRequest()
        user.username = message.author.name
        
        message.mark_read()
        logging.info(f"New Message: {message.author.name} - {message.subject}")

        if re.search(r'stop', message.subject+message.body, re.IGNORECASE):
            user.delete(db)
            message.reply(body="""You have successfully stopped notifications from LFG Notify Bot.  
            If this bot was helpful, please consider making a donation to charity or your GM.""")
            time.sleep(2)

        elif re.search(r'subscribe', message.subject, re.IGNORECASE):
            game = re.findall(game_regex, message.body)
            if not game:
                message.reply(body="""You must include a valid game from the LFG subreddit game tags list https://www.reddit.com/r/lfg/wiki/index/formatting#wiki_game_tags. Other and Flexible LFG tags are not currently supported.  
                &nbsp;   
                ^^For ^^error ^^reporting, ^^please ^^message ^^u/Perfekthuntr.
                """)
                continue

            user.game = ",".join(x.upper() for x in game)

            days = re.findall(day_regex, message.body)
            user.days = ",".join(set(x.upper() for x in days))

            timezone = re.findall(tz_regex, message.body)
            timezone_corrected = set()
            timezone_user= []
            for tz in timezone:
                corrected = time_parser.correct_timezone(tz)
                if corrected:
                    timezone_corrected.add(corrected)
                    if re.search(r"(GMT|UTC)([+-][0-1]?[0-9]:?[0-5]?[0-9]?)", tz, re.IGNORECASE):
                        timezone_user.append(corrected)
                    else:
                        timezone_user.append(f"{tz.upper()} ({corrected})")
                    
            user.timezone = ",".join(timezone_corrected)

            user.nsfw = 1 if re.search(r"nsfw", message.body, re.IGNORECASE) else 0

            user.save(db)

            message.reply(body=f"""You have been successfully subscribed to LFG Notify Bot.  
            &nbsp;  
            Your current settings are:  
            - Timezone(s): {', '.join(timezone_user)}  
            - Game(s): {user.game}  
            - Day(s) of the week: {user.days}  
            - Include NSFW: {'No' if user.nsfw == 0 else 'Yes'}  
            &nbsp;  
            If you wish to change these settings, reply to this message, or reply **STOP** to end notifications.  
            &nbsp;  
            ^^For ^^error ^^reporting, ^^please ^^message ^^u/Perfekthuntr."""
            )
            time.sleep(2)

def main():
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    with Database() as db:
        while True:
            try:
                read_messages(db)
            except prawcore.exceptions.ServerError as err:
                logging.error(f"Server Error: {err}")
                time.sleep(360)
            except praw.exceptions.RedditAPIException as err:
                logging.error(f"API error: {err}")
                time.sleep(120)


if __name__ == "__main__":
    main()