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
    ("Hello World!", Location.NONE.value),
    ("offline", Location.OFFLINE.value),
    ("OFFLINE", Location.OFFLINE.value),
    ("online", Location.ONLINE.value),
    ("[offline] [online]", Location.ONLINE_AND_OFFLINE.value)
]


@pytest.mark.parametrize("text,result", parse_location_data)
def test_parse_location(text, result):
    assert parse_location(text) == result


message_flags_data = [
    ("", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("offline", Location.ONLINE_AND_OFFLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("OFF", Location.ONLINE_AND_OFFLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("=offline", Location.OFFLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("=offline", Location.OFFLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("nsfw", Location.ONLINE.value, Nsfw.INCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("=nsfw", Location.ONLINE.value, Nsfw.ONLY.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("NSFW", Location.ONLINE.value, Nsfw.INCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("pbp", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.ONLY.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("play by post", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.ONLY.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("-pbp", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.EXCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("-play-by-post", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.EXCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("one shot", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.ONLY.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("one-shot", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.ONLY.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("-oneshot", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.EXCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("-one-shot", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.EXCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("lgbtq+", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.ONLY.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("lgbtq", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.ONLY.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("LGBT", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.ONLY.value, AgeLimit.NONE.value, Vtt.NONE.flag),
    ("18+", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.OVER_18.value, Vtt.NONE.flag),
    ("21+", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.OVER_21.value, Vtt.NONE.flag),
    ("anyage", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.ANY_AGE.value, Vtt.NONE.flag),
    ("Roll20", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.ROLL20.flag),
    ("r20", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.ROLL20.flag),
    ("fg", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.FANTASY_GROUNDS.flag),
    ("tts", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.TABLETOP_SIM.flag),
    ("foundry", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.FOUNDRY.flag),
    ("r20 foundry", Location.ONLINE.value, Nsfw.EXCLUDE.value, PlayByPost.INCLUDE.value, OneShot.INCLUDE.value, Lgbtq.INCLUDE.value, AgeLimit.NONE.value, Vtt.ROLL20.flag + Vtt.FOUNDRY.flag),
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
