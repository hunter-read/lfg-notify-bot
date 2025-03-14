import pytest

from model import Location, Nsfw, PlayByPost, OneShot, Identity, AgeLimit, Vtt
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
    ("Meta", 0),
]


@pytest.mark.parametrize("text,result", flair_data)
def test_parse_flair(text, result):
    assert parse_flair(text) == result


parse_location_data = [
    ("Hello World!", Location.NONE.value),
    ("offline", Location.OFFLINE.value),
    ("OFFLINE", Location.OFFLINE.value),
    ("online", Location.ONLINE.value),
    ("[offline] [online]", Location.ONLINE_AND_OFFLINE.value),
]


@pytest.mark.parametrize("text,result", parse_location_data)
def test_parse_location(text, result):
    assert parse_location(text) == result


message_flags_data = [
    (
        "",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "offline",
        Location.ONLINE_AND_OFFLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "OFF",
        Location.ONLINE_AND_OFFLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "=offline",
        Location.OFFLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "=offline",
        Location.OFFLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "nsfw",
        Location.ONLINE.value,
        Nsfw.INCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "=nsfw",
        Location.ONLINE.value,
        Nsfw.ONLY.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "NSFW",
        Location.ONLINE.value,
        Nsfw.INCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "pbp",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.ONLY.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "play by post",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.ONLY.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "-pbp",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.EXCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "-play-by-post",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.EXCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "one shot",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.ONLY.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "one-shot",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.ONLY.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "-oneshot",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.EXCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "-one-shot",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.EXCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "lgbtqplus",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.LGBTQ.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "lgbtplus",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.LGBTQ.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "lgbt+",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.LGBTQ.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "lgbtq+",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.LGBTQ.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "lgbtq",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.LGBTQ.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "LGBT",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.LGBTQ.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "fem",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.FEM.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "poc",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.POC.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "Accessible",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.ACCESSIBLE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "18+",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.OVER_18.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "21+",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.OVER_21.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "anyage",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.ANY_AGE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "Roll20",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.ROLL20.flag,
        False,
        False,
    ),
    (
        "r20",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.ROLL20.flag,
        False,
        False,
    ),
    (
        "fg",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.FANTASY_GROUNDS.flag,
        False,
        False,
    ),
    (
        "tts",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.TABLETOP_SIM.flag,
        False,
        False,
    ),
    (
        "foundry",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.FOUNDRY.flag,
        False,
        False,
    ),
    (
        "talespire",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.TALESPIRE.flag,
        False,
        False,
    ),
    (
        "tableplop",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.TABLEPLOP.flag,
        False,
        False,
    ),
    (
        "sigil",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.SIGIL.flag,
        False,
        False,
    ),
    (
        "theater_mind",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.THEATER_OF_THE_MIND.flag,
        False,
        False,
    ),
    (
        "theater of mind",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.THEATER_OF_THE_MIND.flag,
        False,
        False,
    ),
    (
        "theater of the mind",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.THEATER_OF_THE_MIND.flag,
        False,
        False,
    ),
    (
        "commotion",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        False,
    ),
    (
        "One More Multiverse",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.ONE_MORE_MULTIVERSE.flag,
        False,
        False,
    ),
    (
        "Owlbear Rodeo",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.OWLBEAR_RODEO.flag,
        False,
        False,
    ),
    (
        "Above VTT",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.ABOVE_VTT.flag,
        False,
        False,
    ),
    (
        "abovevtt",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.ABOVE_VTT.flag,
        False,
        False,
    ),
    (
        "r20 foundry",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.ROLL20.flag + Vtt.FOUNDRY.flag,
        False,
        False,
    ),
    (
        "no-tz",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        False,
        True,
    ),
    (
        "no-day",
        Location.ONLINE.value,
        Nsfw.EXCLUDE.value,
        PlayByPost.INCLUDE.value,
        OneShot.INCLUDE.value,
        Identity.NONE.flag,
        AgeLimit.NONE.value,
        Vtt.NONE.flag,
        True,
        False,
    ),
]


@pytest.mark.parametrize("text,location,nsfw,pbp,os,lgbtq,age_limit,vtt,no_day,no_tz", message_flags_data)
def test_parse_message_flags(text, location, nsfw, pbp, os, lgbtq, age_limit, vtt, no_day, no_tz):
    result = parse_message_flags(text)
    assert result.get("location") == location
    assert result.get("nsfw") == nsfw
    assert result.get("play_by_post") == pbp
    assert result.get("one_shot") == os
    assert result.get("lgbtq") == lgbtq
    assert result.get("age_limit") == age_limit
    assert result.get("vtt") == vtt
    assert result.get("match_no_day") == no_day
    assert result.get("match_no_timezone") == no_tz
