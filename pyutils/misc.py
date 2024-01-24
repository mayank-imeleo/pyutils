import math
import time
from datetime import datetime
import random

from dateutil.tz import tzutc


def utc_now():
    return datetime.now(tz=tzutc())


def epoch_now():
    return time.time()


def file_num_lines(filepath):
    return sum(1 for line in open(filepath))


# function to generate OTP
def generate_otp(length=4):
    digits = "0123456789"
    otp = ""
    for i in range(length):
        otp += digits[math.floor(random.random() * len(digits))]
    return otp
