from message_bot import parse_incoming_message
from unittest.mock import MagicMock

from praw.models import Message, Redditor
import pytest

from model import Database, MessageText


username = "TestRedditor"
testUser = Redditor(None, username, None, None)
db = Database("")
db.save = MagicMock()
db.query = MagicMock()


unsubscribe_data = [
    ("subscribe", "STOP"),
    ("New LFG Post", "STOP"),
    ("New LFG Post", "stop"),
    ("subscribe", "unsubscribe"),
    ("New LFG Post", "unsubscribe")
]


@pytest.mark.parametrize("subject,body", unsubscribe_data)
def test_unsubscribe(subject, body):
    message = Message(None, {"id": "12345", "author": testUser, "subject": subject, "body": body, "was_comment": False})
    assert parse_incoming_message(db, message) == MessageText.UNSUBSCRIBE_REPLY
    db.save.assert_called_once_with("DELETE FROM user WHERE username = ?", [username])
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
    message = Message(None, {"id": "12345", "author": testUser, "subject": subject, "body": body, "was_comment": False})
    assert parse_incoming_message(db, message) == MessageText.ERROR_REPLY
    db.save.assert_not_called()
    db.save.reset_mock()


def test_comment_message():
    message = Message(None, {"id": "12345", "author": testUser, "subject": "", "body": "Hello World!", "was_comment": True})
    assert parse_incoming_message(db, message) == MessageText.COMMENT_REPLY
    db.save.assert_not_called()
    db.save.reset_mock()


def test_unknown_message():
    message = Message(None, {"id": "12345", "author": testUser, "subject": "New LFG post matching your criteria", "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "was_comment": False})
    assert parse_incoming_message(db, message) == MessageText.UNKNOWN_MESSAGE_REPLY
    db.save.assert_not_called()
    db.save.reset_mock()


def test_no_game_subscribe_message():
    message = Message(None, {"id": "12345", "author": testUser, "subject": "Subscribe", "body": "GMT-9,GMT-8,GMT-7 Monday/Wednesday/Weekends NSFW", "was_comment": False})
    assert parse_incoming_message(db, message) == MessageText.MISSING_GAME_REPLY
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
def test_subscribe_new_user(subject, body, reply_text, db_data):
    db.query = MagicMock(return_value=[(0,)])
    message = Message(None, {"id": "12345", "author": testUser, "subject": subject, "body": body, "was_comment": False})
    assert parse_incoming_message(db, message) == (f"You have been successfully subscribed to LFG Notify Bot.  \n"
                                                   "&nbsp;  \n"
                                                   "Your current settings are:  \n"
                                                   f"- Game: {reply_text[0]}  \n"
                                                   f"- Timezone: {reply_text[1]}  \n"
                                                   f"- Day of the week: {reply_text[2]}  \n"
                                                   f"- Include NSFW: {reply_text[3]}  \n"
                                                   "&nbsp;  \n"
                                                   "If you wish to change these settings, reply to this message (include all settings, not just your updates), or reply **STOP** to end notifications.  \n"
                                                   "&nbsp;  \n"
                                                   "^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/user/Perfekthuntr)")
    db.query.assert_any_call("SELECT EXISTS (SELECT id FROM user WHERE username = ?)", [username])
    db.save.assert_called_with("INSERT INTO user (game, timezone, day, nsfw, keyword, flair, username) VALUES (?, ?, ?, ?, ?, ?, ?)", [db_data[0], db_data[1], db_data[2], db_data[3], None, 3, username])
    db.save.reset_mock()
    db.query.reset_mock()


@pytest.mark.parametrize("subject,body,reply_text,db_data", subscribe_data)
def test_subscribe_existing_user(subject, body, reply_text, db_data):
    db.query = MagicMock(return_value=[(1,)])
    message = Message(None, {"id": "12345", "author": testUser, "subject": subject, "body": body, "was_comment": False})
    assert parse_incoming_message(db, message) == (f"You have been successfully subscribed to LFG Notify Bot.  \n"
                                                   "&nbsp;  \n"
                                                   "Your current settings are:  \n"
                                                   f"- Game: {reply_text[0]}  \n"
                                                   f"- Timezone: {reply_text[1]}  \n"
                                                   f"- Day of the week: {reply_text[2]}  \n"
                                                   f"- Include NSFW: {reply_text[3]}  \n"
                                                   "&nbsp;  \n"
                                                   "If you wish to change these settings, reply to this message (include all settings, not just your updates), or reply **STOP** to end notifications.  \n"
                                                   "&nbsp;  \n"
                                                   "^^For ^^error ^^reporting, ^^please ^^message ^^my [^^human.](https://www.reddit.com/user/Perfekthuntr)")
    db.query.assert_any_call("SELECT EXISTS (SELECT id FROM user WHERE username = ?)", [username])
    db.save.assert_called_with("UPDATE user SET date_updated = CURRENT_TIMESTAMP, game = ?, timezone = ?, day = ?, nsfw = ?, keyword = ?, flair = ? WHERE username = ?", [db_data[0], db_data[1], db_data[2], db_data[3], None, 3, username])
    db.save.reset_mock()
    db.query.reset_mock()
