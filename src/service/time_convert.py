import re


def to_gmt(time: str, timezone: str) -> str:
    return __convert_by_timezone(time, timezone, "+")


def to_timezone(time: str, timezone: str) -> str:
    return __convert_by_timezone(time, timezone, "-")


def convert_time_across_timezones(time: str, input_timezone: str, output_timezone: str) -> str:
    gmt_time = to_gmt(time, input_timezone)
    day_change = None
    if gmt_time.endswith("+") or gmt_time.endswith("-"):
        day_change = gmt_time[4:]
        gmt_time = gmt_time[:4]

    new_time = to_timezone(gmt_time, output_timezone)
    if day_change and (new_time.endswith("+") or new_time.endswith("-")):
        return new_time[:4]
    elif day_change:
        return f"{new_time}{day_change}"
    else:
        return new_time


def __convert_by_timezone(time: str, timezone: str, direction: chr) -> str:
    time = int(time)
    hours = time // 100
    minutes = time % 100
    match = re.search(r"GMT([+-])([0-1]?[0-9]):?(00|15|30|45)?", timezone)
    tz_hours = int(match.group(2))
    tz_minutes = int(match.group(3)) if match.group(3) else 0
    if match.group(1) == direction:
        tz_hours *= -1
        tz_minutes *= -1
    hours += tz_hours
    minutes += tz_minutes
    if minutes >= 60:
        minutes -= 60
        hours += 1
    elif minutes < 0:
        minutes += 60
        hours -= 1

    if hours >= 24:
        return f"{(hours - 24):02d}{minutes:02d}+"
    elif hours < 0:
        return f"{(hours + 24):02d}{minutes:02d}-"

    return f"{hours:02d}{minutes:02d}"
