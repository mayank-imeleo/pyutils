from datetime import datetime

import pendulum


class DateTimeFormats:
    ddmonyyyy = "%d-%b-%Y"


def ddmonyyyy_to_datetime(ddmonyyyy):
    return datetime.strptime(ddmonyyyy, DateTimeFormats.ddmonyyyy)


def datetime_to_datetime_str(dt, tz="UTC"):
    return pendulum.instance(dt).in_tz(tz).format("YYYY-MM-DD hh:mm:ss A")


def datetime_to_time_str(dt, tz="UTC"):
    return pendulum.instance(dt).in_tz(tz).format("hh:mm:ss A")


def dt_add_mins(dt, mins):
    return pendulum.instance(dt).add(minutes=mins)
