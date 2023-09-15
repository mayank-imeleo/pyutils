from datetime import datetime, timedelta, time

from dateutil.tz import tzutc
from django.db.models import Manager


class TimeStampedModelManager(Manager):
    def records_today(self):
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time(), tzutc())
        today_end = datetime.combine(tomorrow, time(), tzutc())
        return self.filter(created__lte=today_end, created__gte=today_start)
