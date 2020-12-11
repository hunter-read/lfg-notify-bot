from enum import Enum


class MessageText(str, Enum):
    COMMENT_REPLY = ("Hello, if you want to [use my features](https://github.com/hunter-read/lfg-notify-bot/blob/main/README.md), please [send a message to me](https://www.reddit.com/message/compose/?to=LFG_Notify_Bot) to subscribe.  "
                     "I currently do not support submission tagging  "
                     "&nbsp;  \n"
                     "^^This ^^comment ^^was ^^done ^^automatically. ^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/user/Perfekthuntr)")

    UNSUBSCRIBE_REPLY = ("You have successfully stopped notifications from LFG Notify Bot.  \n"
                         "If this bot was helpful, please let me know that I was a [good bot here](https://www.reddit.com/user/LFG_Notify_Bot/comments/jxsf6t/accolades_and_success_stories/) and leave some feedback so my human can improve me.  \n"
                         "&nbsp;  \n"
                         "^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/user/Perfekthuntr)")

    ERROR_REPLY = "For error reporting or [feature requests](), please message my [human](https://www.reddit.com/user/Perfekthuntr)."

    MISSING_GAME_REPLY = ("You must include a valid game from the [LFG subreddit game tags list](https://www.reddit.com/r/lfg/wiki/index/formatting#wiki_game_tags).  \n"
                          "Examples include 5e, CoC, GURPS, or PF1e. Other and Flexible LFG tags are not currently supported.  \n"
                          "&nbsp;  \n"
                          "^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/user/Perfekthuntr)")

    UNKNOWN_MESSAGE_REPLY = ("Unknown message sent. If you wish to subscribe to this bot, please send a new message titled 'Subscribe' with your [options](https://github.com/hunter-read/lfg-notify-bot/blob/main/README.md) in the body of the message.  \n"
                             "If you wish to end notifications reply **STOP** to any message, or send a new message titled 'Stop'.  \n"
                             "&nbsp;  \n"
                             "^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/user/Perfekthuntr)")

    SUBMISSION_NOTIFICATION_SUBJECT = "New LFG post matching your criteria"
    SUBMISSION_NOTIFICATION_BODY = ("&nbsp;  \n"
                                    "Reply **STOP** to end notifications.  \n"
                                    "&nbsp;  \n"
                                    "^Reminder ^that ^all ^information ^provided ^is ^a ^best ^guess, ^and ^you ^should ^read ^the ^post ^linked ^above")

    OVERLIMIT_NOTIFICATION_SUBJECT = "Your notifications from LFG Notification Bot have been automatically stopped"
    OVERLIMIT_NOTIFICATION_BODY = ("You have reached the max number of notifications from LFG Notification Bot with your current settings and have been unsubscribed from the service. "
                                   "If you have only been subscribed for a short while, you may need to limit your search filters more.  \n"
                                   "You may [resubscribe at any time by sending a new message](https://www.reddit.com/message/compose/?to=LFG_Notify_Bot) titled 'Subscribe' with your [options](https://github.com/hunter-read/lfg-notify-bot/blob/main/README.md).  \n"
                                   "&nbsp;  \n"
                                   "^^This ^^action ^^was ^^done ^^automatically. ^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/user/Perfekthuntr)")
