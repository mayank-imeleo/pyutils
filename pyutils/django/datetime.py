from django.conf import settings
from django.utils.timezone import now

from pyutils.datetime import datetime_to_time_str, datetime_to_datetime_str


def now_date():
    return now().date()


def now_hour():
    return now().hour


def now_minute():
    return now().minute


def local_time_str(dt=now()):
    return datetime_to_time_str(dt, tz=settings.LOCAL_TIME_ZONE)


def local_datetime_str(dt=now()):
    return datetime_to_datetime_str(dt, tz=settings.LOCAL_TIME_ZONE)
