import logging

from django.conf import settings
from django.utils.timezone import now
from import_export.formats.base_formats import CSV
from import_export.resources import ModelResource

from pyutils.datetime import datetime_to_datetime_str, datetime_to_time_str

logger = logging.getLogger(__name__)


class ImportExportCSVFormatMixin:
    formats = [CSV]


class CustomModelResource(ModelResource):
    def after_import_instance(self, row, row_result, row_number=None, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        """
        m = self._meta.model.__name__
        f = kwargs["file_name"]
        n = row_number
        logger.debug(f"{m} Added | File:{f} | Row:{n}")


def local_time_str(dt=now()):
    return datetime_to_time_str(dt, tz=settings.LOCAL_TIME_ZONE)


def local_datetime_str(dt=now()):
    return datetime_to_datetime_str(dt, tz=settings.LOCAL_TIME_ZONE)
