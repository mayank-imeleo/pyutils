from typing import List

from django.template.defaultfilters import slugify


class PageAutoFieldsMixin:
    @property
    def auto_fields(self) -> List:
        raise NotImplementedError

    @property
    def auto_title(self):
        return "-".join(self.auto_fields)

    @property
    def auto_slug(self):
        return slugify("-".join(self.auto_fields))
