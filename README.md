# Reddit LFG Notification Bot
This is the source for the https://www.reddit.com/user/LFG_Notify_Bot

## Purpose

I am a bot that aims to make using r/lfg easier to use and provide notifications when a tabletop game that meets your criteria is posted on reddit. It can be hard to find a game that matches your schedule or plays a tabletop game that is uncommon. And unless you are lucky, have an open schedule, or are able to stalk the subreddit, it can be difficult to find a game. So I am here to help with that endeavor.

I am still in beta, but if this interests you, [send me a message](https://www.reddit.com/message/compose/?to=LFG_Notify_Bot)  with the title Subscribe and in the body include the following:

* Game: Any game in the [LFG subreddit game tags](https://www.reddit.com/r/lfg/wiki/index/formatting#wiki_game_tags) list ("Flexible" and "Other" game tags are not supported yet)
* Timezone: Most of the Europe, North America, and Australian time zone 3 or 4 character codes are support, as is any GMT+# or UTC+# format. (Not Required, but you will be notified more frequently if not included)
* Day of the Week: Monday, Tuesday, Friday (It is reccomended to use full day of week text, ie. Monday not Mon)
* NSFW: By default all nsfw posts are excluded, if you are okay with nsfw posts, then include "nsfw" in the message

You can include as many games, timezones, or days of the week as you want and I will send you a message when someone posts a game looking for player's that meets your criteria, but currently I only search for posts with [Online] and the flairs "GM and player(s) wanted" or "Player(s) wanted".

Example message body
```
5e, PF2e
Monday, Wednesday
PST, GMT-7
```
```
40k 5E gurps
thursdays \ Friday
utc utc+1
nsfw
```

## Notes
While this bot does it's best to parse a user post, due to inconsistencies in how people post, there is no guarantee that the data it collects is 100% accurate. While the bot does try it's best, the very nature of text parsing is difficult and even if I were to try and use some sort of machine learning, there would still be issues. I recommend if you subscribe to this bot, to read through any post it thinks is applicable to your settings. If you see a blatent issue, please add an issue to the github page, or send [u/Perfekthuntr](https://www.reddit.com/user/Perfekthuntr) a message on reddit and I will do my best to investigate.

## Workings
Currently I am 2 bots, one that reads incoming user messages and another that parses and notifies users on submissions. The user requests are stored in a simple Sqlite database as is some post information for fun data collection.

Requirements:
* python 3.7+
* praw (`pip3 install praw`)
* pytest (For unit tests: `pip3 install pytest`)

## Future improvements / Known issues
* Alternate game name support
* Day/Time timezone manipulation

## License
LFG Notification Bot provided under the [Simplified BSD License](https://github.com/hunter-read/lfg-notify-bot/blob/main/LICENSE)
