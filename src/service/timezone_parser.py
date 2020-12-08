import re
import typing


__tz_dict = {
    "GMT": "GMT+0",
    "UTC": "GMT+0",
    "ADT": "GMT-3",
    "AST": "GMT-4",
    "AKDT": "GMT-8",
    "AKST": "GMT-9",
    "CDT": "GMT-5",
    "CST": "GMT-6",
    "CT": "GMT-5,GMT-6",
    "EDT": "GMT-4",
    "EGST": "GMT+0",
    "EGT": "GMT-1",
    "EST": "GMT-5",
    "ET": "GMT-4,GMT-5",
    "HDT": "GMT-9",
    "HST": "GMT-10",
    "MDT": "GMT-6",
    "MST": "GMT-7",
    "MT": "GMT-6,GMT-7",
    "PDT": "GMT-7",
    "PST": "GMT-8",
    "PT": "GMT-7,GMT-8",
    "BST": "GMT+1",
    "CEST": "GMT+2",
    "CET": "GMT+1",
    "EEST": "GMT+3",
    "EET": "GMT+2",
    # "WEST": "GMT+01",
    "WET": "GMT+0",
    "ACDT": "GMT+10:30",
    "ACST": "GMT+9:30",
    "ACT": "GMT+10:30,GMT+9:30",
    "AEDT": "GMT+11",
    "AEST": "GMT+10",
    "AET": "GMT+10,GMT+11",
    "AWDT": "GMT+9",
    "AWST": "GMT+8"
}
__tz_regex = re.compile(r"\b((?:GMT|UTC)\s?(?:[+-][0-1]?[0-9]:?[0-5]?[0-9]?)?|(?:ADT|AKDT|AKST|AST|CDT|CST|EDT|EGST|EGT|EST|HDT|HST|MDT|MST|MT|PDT|PST|BST|CEST|CET|EEST|EET|WET|ACDT|ACST|ACT|AEDT|AEST|AET|AWDT|AWST)\b)", flags=re.IGNORECASE)
__gmt_catch_regex = re.compile(r"(?:GMT|UTC)\s?([+-])([0-1]?[0-9]):?(00|30|45)?", flags=re.IGNORECASE)


def parse_timezone(text: str) -> typing.Set[str]:
    text = text.replace("\u2212", "-")
    return set([i.strip().upper() for i in re.findall(__tz_regex, text)])


def timezone_to_gmt(tz: str) -> str:
    match = re.search(__gmt_catch_regex, tz)
    if match:
        if match.group(3):
            return f"GMT{match.group(1)}{int(match.group(2))}:{match.group(3)}"
        return f"GMT{match.group(1)}{int(match.group(2))}"
    return __tz_dict.get(tz.upper(), None)
