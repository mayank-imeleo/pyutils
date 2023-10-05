import uuid
from typing import List

from django.template.defaultfilters import slugify
from treebeard.exceptions import NodeAlreadySaved
from wagtail.models import Page


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


class BasePage(Page):
    def get_uid(self):
        """
        Returns a value that uniquely identifies the page object
        :return:
        """
        return uuid.uuid4()

    def set_title(self):
        self.title = f"{self.__class__.__name__}-{self.get_uid()}"

    def set_parent_page(
        self,
    ):
        """
        Adds path and depth to child page
        """
        if child_has_parent(self):
            return
        parent_page_class = getattr(self, "parent_page_types")[0]
        wagtail_page = Page.objects.type(parent_page_class).first()
        _attr = parent_page_class._meta.verbose_name.replace(" ", "")
        parent_page = getattr(wagtail_page, _attr)
        try:
            parent_page.add_child(instance=self)
        except NodeAlreadySaved:
            pass

    def save(self, clean=True, user=None, log_action=False, **kwargs):
        self.set_title()
        self.set_parent_page()

    class Meta:
        abstract = True


def child_has_parent(child):
    return child.depth and child.path
