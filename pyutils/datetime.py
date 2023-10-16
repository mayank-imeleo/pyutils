from datetime import datetime


class DateTimeFormats:
    ddmonyyyy = "%d-%b-%Y"


def ddmonyyyy_to_datetime(ddmonyyyy):
    return datetime.strptime(ddmonyyyy, DateTimeFormats.ddmonyyyy)
