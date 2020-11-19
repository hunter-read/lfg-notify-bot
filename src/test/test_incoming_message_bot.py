import pytest
from unittest.mock import MagicMock
from incoming_message_bot import parse_incoming_message
from praw.models import Message, Redditor
from model import Database

username = "TestRedditor"
testUser = Redditor(None, username, None, None)
db = Database("")
db.save = MagicMock()

unsubscribe_data = [
    ("subscribe", "STOP"),
    ("New LFG Post", "STOP"),
    ("New LFG Post", "stop"),
    ("subscribe", "unsubscribe"),
    ("New LFG Post", "unsubscribe")
]


@pytest.mark.parametrize("subject,body", unsubscribe_data)
def test_unsubscribe(subject, body):
    message = Message(None, {"id": "12345", "author": testUser, "subject": subject, "body": body})
    assert parse_incoming_message(db, message) == ("You have successfully stopped notifications from LFG Notify Bot.  \n"
                                                   "If this bot was helpful, please consider making a donation to charity or your GM.")
    db.save.assert_called_once_with("DELETE FROM user_request WHERE username = ?", [username])
    db.save.reset_mock()


bug_feature_data = [
    ("subscribe", "bug"),
    ("New LFG Post", "issue"),
    ("New LFG Post", "error"),
    ("suggestion", "Other text"),
    ("feature", "More text")
]


@pytest.mark.parametrize("subject,body", bug_feature_data)
def test_bug_feature_message(subject, body):
    message = Message(None, {"id": "12345", "author": testUser, "subject": subject, "body": body})
    assert parse_incoming_message(db, message) == "For error reporting or feature requests, please message u/Perfekthuntr."
    db.save.assert_not_called()
    db.save.reset_mock()


def test_unknown_message():
    message = Message(None, {"id": "12345", "author": testUser, "subject": "New LFG post matching your criteria", "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."})
    assert parse_incoming_message(db, message) == ("Unknown message sent. If you wish to subscribe to this bot, please send a new message titled 'Subscribe' with your options in the body of the message.  \n"
                                                   "If you wish to end notifications reply **STOP** to any message, or send a new message titled 'Stop'.  \n"
                                                   "&nbsp;  \n"
                                                   "^^For ^^error ^^reporting, ^^please ^^message ^^u/Perfekthuntr.")
    db.save.assert_not_called()
    db.save.reset_mock()


def test_no_game_subscribe_message():
    message = Message(None, {"id": "12345", "author": testUser, "subject": "Subscribe", "body": "GMT-9,GMT-8,GMT-7 Monday/Wednesday/Weekends NSFW"})
    assert parse_incoming_message(db, message) == ("You must include a valid game from the LFG subreddit game tags list https://www.reddit.com/r/lfg/wiki/index/formatting#wiki_game_tags.  \n"
                                                   "Examples include 5e, CoC, GURPS, or PF1e. Other and Flexible LFG tags are not currently supported.  \n"
                                                   "&nbsp;  \n"
                                                   "^^For ^^error ^^reporting, ^^please ^^message ^^u/Perfekthuntr.")
    db.save.assert_not_called()
    db.save.reset_mock()


subscribe_data = [
    ("subscribe", "5e\nPST Wed NSFW", ["5E", "PST (GMT-8)", "Wednesday", "Yes"], ["5E", "GMT-8", "WEDNESDAY", 1]),
    ("subscribe", "CoC", ["COC", "None Input", "None Input", "No"], ["COC", None, None, 0]),
    ("lfg", "5e\nPST Wed NSFW", ["5E", "PST (GMT-8)", "Wednesday", "Yes"], ["5E", "GMT-8", "WEDNESDAY", 1]),
    ("notify", "5e\nPST Wed NSFW", ["5E", "PST (GMT-8)", "Wednesday", "Yes"], ["5E", "GMT-8", "WEDNESDAY", 1]),
    ("CoC", "PST Wed NSFW", ["COC", "PST (GMT-8)", "Wednesday", "Yes"], ["COC", "GMT-8", "WEDNESDAY", 1])
]


@pytest.mark.parametrize("subject,body,reply_text,db_data", subscribe_data)
def test_subscribe(subject, body, reply_text, db_data):
    message = Message(None, {"id": "12345", "author": testUser, "subject": subject, "body": body})
    assert parse_incoming_message(db, message) == (f"You have been successfully subscribed to LFG Notify Bot.  \n"
                                                   "&nbsp;  \n"
                                                   "Your current settings are:  \n"
                                                   f"- Game(s): {reply_text[0]}  \n"
                                                   f"- Timezone(s): {reply_text[1]}  \n"
                                                   f"- Day(s) of the week: {reply_text[2]}  \n"
                                                   f"- Include NSFW: {reply_text[3]}  \n"
                                                   "&nbsp;  \n"
                                                   "If you wish to change these settings, reply to this message, or reply **STOP** to end notifications.  \n"
                                                   "&nbsp;  \n"
                                                   "^^For ^^error ^^reporting, ^^please ^^message ^^u/Perfekthuntr.")
    db.save.assert_any_call("DELETE FROM user_request WHERE username = ?", [username])
    db.save.assert_called_with("INSERT INTO user_request (id, date_created, username, game, timezone, day_of_week, nsfw) VALUES (null, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)", [username, db_data[0], db_data[1], db_data[2], db_data[3]])
    db.save.reset_mock()
