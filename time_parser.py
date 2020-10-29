import re

tz_dict = {
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
    "WEST": "GMT+1",
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

def correct_timezone(tz):
    gmt_catch = re.compile(r"(?:GMT|UTC)([+-][0-1]?[0-9]:?[0-5]?[0-9]?)", flags=re.IGNORECASE)
    match = re.search(gmt_catch, tz)
    if match:
        return f"GMT{match.group(1)}"
    return tz_dict.get(tz.upper())


def to_military_time(time):
    hours = -1
    minutes = -1

    m = re.match(r'([0-2][0-9]):?([0-5][0-9])', time)
    if m:
        hours = int(m.group(1))
        minutes = int(m.group(2))

    m = re.match(r'([0-2]?[0-9]):?([0-5][0-9])?\s*(am|pm)', time, re.IGNORECASE)
    if m:
        hours = int(m.group(1))
        if (m.group(2)):
            minutes = int(m.group(2))
        else:
            minutes = 0
        if re.match(m.group(3), 'pm', re.IGNORECASE) and hours != 12:
            hours += 12
        elif re.match(m.group(3), 'am', re.IGNORECASE) and hours == 12:
            hours = 0

    if hours == -1 or minutes == -1:
        return None
        
    return str(hours)+str(minutes)