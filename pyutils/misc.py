import time
from datetime import datetime

from dateutil.tz import tzutc


def utc_now():
    return datetime.now(tz=tzutc())


def epoch_now():
    return time.time()


def file_num_lines(filepath):
    return sum(1 for line in open(filepath))
