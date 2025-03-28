from enum import Enum
from re import escape


class MessageText(str, Enum):
    COMMENT_REPLY = (
        "Hello, if you want to [use my features](https://github.com/hunter-read/lfg-notify-bot/blob/main/README.md), please [send a message to me](https://www.reddit.com/message/compose/?to=LFG_Notify_Bot) to subscribe.  "
        "I currently do not support submission tagging  "
        "&nbsp;  \n"
        "^^This ^^comment ^^was ^^done ^^automatically. ^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/user/Perfekthuntr)"
    )

    UNSUBSCRIBE_REPLY = (
        "You have successfully stopped notifications from LFG Notify Bot. Please allow 1 hour for any residual messages to propogate through the system.  \n"
        "&nbsp;  \n"
        "^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/message/compose/?to=Perfekthuntr&subject=LFG%20Notification%20Bot%20Issue)"
    )

    ERROR_REPLY = "For error reporting or [feature requests](), please message my [human](https://www.reddit.com/message/compose/?to=Perfekthuntr&subject=LFG%20Notification%20Bot%20Issue)."

    MISSING_GAME_REPLY = (
        "You must include a valid game from the [LFG subreddit game tags list](https://www.reddit.com/r/lfg/wiki/index/formatting#wiki_game_tags).  \n"
        "Examples include 5e, CoC, GURPS, or PF1e. Other and Flexible LFG tags are not currently supported.  \n"
        "&nbsp;  \n"
        "^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/message/compose/?to=Perfekthuntr&subject=LFG%20Notification%20Bot%20Issue)"
    )

    UNKNOWN_MESSAGE_REPLY = (
        "Unknown message sent. If you wish to subscribe to this bot, please send a new message titled 'Subscribe' with your [options](https://github.com/hunter-read/lfg-notify-bot/blob/main/README.md) in the body of the message.  \n"
        "If you wish to end notifications reply **STOP** to any message, or send a new message titled 'Stop'.  \n"
        "&nbsp;  \n"
        "^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/message/compose/?to=Perfekthuntr&subject=LFG%20Notification%20Bot%20Issue)"
    )

    SUBMISSION_NOTIFICATION_SUBJECT = "New LFG post matching your criteria"
    SUBMISSION_NOTIFICATION_BODY = (
        "&nbsp;  \n"
        "Reply **STOP** to end notifications.  \n"
        "&nbsp;  \n"
        "^Reminder ^that ^all ^information ^provided ^is ^a ^best ^guess, ^and ^you ^should ^read ^the ^post ^linked ^above.  \n"
        "^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/message/compose/?to=Perfekthuntr&subject=LFG%20Notification%20Bot%20Issue)"
    )

    OVERLIMIT_NOTIFICATION_SUBJECT = "Your notifications from LFG Notification Bot have been automatically stopped"
    OVERLIMIT_NOTIFICATION_BODY = (
        "You have reached the max number of notifications from LFG Notification Bot with your current settings and have been unsubscribed from the service. "
        "If you have only been subscribed for a short while, you may need to limit your search filters more.  \n"
        "You may [resubscribe at any time by sending a new message](https://www.reddit.com/message/compose/?to=LFG_Notify_Bot) titled 'Subscribe' with your [options](https://github.com/hunter-read/lfg-notify-bot/blob/main/README.md).  \n"
        "&nbsp;  \n"
        "^^This ^^action ^^was ^^done ^^automatically. ^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/message/compose/?to=Perfekthuntr&subject=LFG%20Notification%20Bot%20Issue)"
    )


class Flair(Enum):
    PLAYERS_WANTED = (1, "Player(s) wanted")
    GM_AND_PLAYERS_WANTED = (2, "GM and Player(s) wanted")
    GM_WANTED = (4, "GM wanted")
    DEFAULT = (3, None)

    def __init__(self, flag: int, string: str):
        self.flag = flag
        self.string = string

    @classmethod
    def flag_to_str(cls, flag: int) -> str:
        strings = []
        flag & cls.PLAYERS_WANTED.flag and strings.append(cls.PLAYERS_WANTED.string)
        flag & cls.GM_AND_PLAYERS_WANTED.flag and strings.append(cls.GM_AND_PLAYERS_WANTED.string)
        flag & cls.GM_WANTED.flag and strings.append(cls.GM_WANTED.string)
        return ", ".join(strings)

    @property
    def regex_str(self) -> str:
        return escape(self.string)


class Vtt(Enum):
    NONE = (0, None)
    ROLL20 = (1, "Roll20")
    FANTASY_GROUNDS = (2, "Fantasy Grounds")
    TABLETOP_SIM = (4, "Tabletop Simulator")
    FOUNDRY = (8, "Foundry VTT")
    # ASTRAL = (16, "Astral Tabletop") # Astral is Defunct - Leaving here for posterity
    TABLEPLOP = (32, "TablePlop")
    TALESPIRE = (64, "TaleSpire")
    ONE_MORE_MULTIVERSE = (128, "One More Multiverse")
    OWLBEAR_RODEO = (256, "Owlbear Rodeo")
    ABOVE_VTT = (512, "Above VTT")
    SIGIL = (1024, "Sigil")
    THEATER_OF_THE_MIND = (2048, "Theater of the Mind")

    def __init__(self, flag: int, string: str):
        self.flag = flag
        self.string = string

    @classmethod
    def flag_to_str_array(cls, flag: int) -> list:
        strings = []
        flag & cls.ROLL20.flag and strings.append(cls.ROLL20.string)
        flag & cls.FANTASY_GROUNDS.flag and strings.append(cls.FANTASY_GROUNDS.string)
        flag & cls.TABLETOP_SIM.flag and strings.append(cls.TABLETOP_SIM.string)
        flag & cls.FOUNDRY.flag and strings.append(cls.FOUNDRY.string)
        flag & cls.TABLEPLOP.flag and strings.append(cls.TABLEPLOP.string)
        flag & cls.TALESPIRE.flag and strings.append(cls.TALESPIRE.string)
        flag & cls.ONE_MORE_MULTIVERSE.flag and strings.append(cls.ONE_MORE_MULTIVERSE.string)
        flag & cls.OWLBEAR_RODEO.flag and strings.append(cls.OWLBEAR_RODEO.string)
        flag & cls.ABOVE_VTT.flag and strings.append(cls.ABOVE_VTT.string)
        flag & cls.SIGIL.flag and strings.append(cls.SIGIL.string)
        flag & cls.THEATER_OF_THE_MIND.flag and strings.append(cls.THEATER_OF_THE_MIND.string)
        return strings


class Location(Enum):
    ONLINE = 1
    ONLINE_AND_OFFLINE = 0
    OFFLINE = -1
    NONE = -9

    def __int__(self):
        return self.value


class Nsfw(Enum):
    EXCLUDE = -1
    INCLUDE = 0
    ONLY = 1

    def __int__(self):
        return self.value


class PlayByPost(Enum):
    EXCLUDE = -1
    INCLUDE = 0
    ONLY = 1

    def __int__(self):
        return self.value


class OneShot(Enum):
    EXCLUDE = -1
    INCLUDE = 0
    ONLY = 1

    def __int__(self):
        return self.value


class Identity(Enum):
    NONE = (0, None)
    LGBTQ = (1, "LGBTQ+")
    FEM = (2, "Feminine or Woman")
    POC = (4, "Person of Color")
    ACCESSIBLE = (8, "Accessible")

    def __init__(self, flag: int, string: str):
        self.flag = flag
        self.string = string

    @classmethod
    def flag_to_str_array(cls, flag: int) -> list:
        strings = []
        flag & cls.LGBTQ.flag and strings.append(cls.LGBTQ.string)
        flag & cls.FEM.flag and strings.append(cls.FEM.string)
        flag & cls.POC.flag and strings.append(cls.POC.string)
        flag & cls.ACCESSIBLE.flag and strings.append(cls.ACCESSIBLE.string)
        return strings


class AgeLimit(Enum):
    ANY_AGE = -1
    NONE = 0
    OVER_18 = 18
    OVER_21 = 21

    def __int__(self):
        return self.value

    @classmethod
    def tostring(cls, val: int) -> str:
        if val == cls.ANY_AGE.value:
            return "No age limit"
        if val == cls.OVER_18.value:
            return "18+"
        if val == cls.OVER_21.value:
            return "21+"
        return None
