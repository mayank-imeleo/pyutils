import time
from datetime import datetime

from dateutil.tz import tzutc
from inflection import dasherize, underscore


def pc2dc(s: str):
    """
    PascalCase to dash-case
    """
    return dasherize(underscore(s))


def pc2uc(s: str):
    """
    PascalCase" to "underscore_case
    """
    return underscore(s)


def utc_now():
    return datetime.now(tz=tzutc())


def epoch_now():
    return time.time()


def string_to_int(string):
    """
    '1k' -> 1000
    '1M' -> 1000000
    :param string:
    :return:
    """
    multipliers = {"K": 1000, "M": 1000000, "B": 1000000000}
    if string[-1].isdigit():  # check if no suffix
        return int(string)
    mult = multipliers[string[-1].upper()]  # look up suffix to get multiplier
    # convert number to float, multiply by multiplier, then make int
    return int(float(string[:-1]) * mult)


def file_num_lines(filepath):
    return sum(1 for line in open(filepath))
