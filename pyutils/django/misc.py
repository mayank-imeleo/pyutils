import logging

from import_export.formats.base_formats import CSV
from import_export.resources import ModelResource

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
