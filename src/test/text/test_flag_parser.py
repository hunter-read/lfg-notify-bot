import pytest

from model import Location, Nsfw, PlayByPost, OneShot, Lgbtq, AgeLimit, Vtt
from text import parse_flair, parse_location, parse_message_flags


flair_data = [
    (None, 0),
    ("Player(s) wanted", 1),
    ("Player wanted", 1),
    ("Players wanted", 1),
    ("plw", 1),
    ("GM and player(s) wanted", 2),
    ("gmplw", 2),
    ("GM wanted", 4),
    ("gmw", 4),
    ("GM and player(s) wanted, Player(s) wanted", 3),
    ("GM and player(s) wanted, Player(s) wanted, GM wanted", 7),
    ("Meta", 0)
]


@pytest.mark.parametrize("text,result", flair_data)
def test_parse_flair(text, result):
    assert parse_flair(text) == result


parse_location_data = [
    ("Hello World!", Location.NONE),
    ("offline", Location.OFFLINE),
    ("OFFLINE", Location.OFFLINE),
    ("online", Location.ONLINE),
    ("[offline] [online]", Location.ONLINE_AND_OFFLINE)
]


@pytest.mark.parametrize("text,result", parse_location_data)
def test_parse_location(text, result):
    assert parse_location(text) == result


message_flags_data = [
    ("", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("offline", Location.ONLINE_AND_OFFLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("OFF", Location.ONLINE_AND_OFFLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("=offline", Location.OFFLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("=offline", Location.OFFLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("nsfw", Location.ONLINE, Nsfw.INCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("=nsfw", Location.ONLINE, Nsfw.ONLY, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("NSFW", Location.ONLINE, Nsfw.INCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("pbp", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.ONLY, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("play by post", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.ONLY, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("-pbp", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.EXCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("-play-by-post", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.EXCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("one shot", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.ONLY, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("one-shot", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.ONLY, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("-oneshot", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.EXCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("-one-shot", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.EXCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.NONE.flag),
    ("lgbtq+", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.ONLY, AgeLimit.NONE, Vtt.NONE.flag),
    ("lgbtq", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.ONLY, AgeLimit.NONE, Vtt.NONE.flag),
    ("LGBT", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.ONLY, AgeLimit.NONE, Vtt.NONE.flag),
    ("18+", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.OVER_18, Vtt.NONE.flag),
    ("21+", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.OVER_21, Vtt.NONE.flag),
    ("anyage", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.ANY_AGE, Vtt.NONE.flag),
    ("Roll20", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.ROLL20.flag),
    ("r20", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.ROLL20.flag),
    ("fg", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.FANTASY_GROUNDS.flag),
    ("tts", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.TABLETOP_SIM.flag),
    ("foundry", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.FOUNDRY.flag),
    ("r20 foundry", Location.ONLINE, Nsfw.EXCLUDE, PlayByPost.INCLUDE, OneShot.INCLUDE, Lgbtq.INCLUDE, AgeLimit.NONE, Vtt.ROLL20.flag + Vtt.FOUNDRY.flag),
]


@pytest.mark.parametrize("text,location,nsfw,pbp,os,lgbtq,age_limit,vtt", message_flags_data)
def test_parse_message_flags(text, location, nsfw, pbp, os, lgbtq, age_limit, vtt):
    result = parse_message_flags(text)
    assert result.get("location") == location
    assert result.get("nsfw") == nsfw
    assert result.get("play_by_post") == pbp
    assert result.get("one_shot") == os
    assert result.get("lgbtq") == lgbtq
    assert result.get("age_limit") == age_limit
    assert result.get("vtt") == vtt
