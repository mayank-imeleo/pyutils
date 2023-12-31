import uuid
from typing import List

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template.defaultfilters import slugify
from treebeard.exceptions import NodeAlreadySaved
from wagtail.images.models import Image
from wagtail.models import Page
from wagtail.utils.file import hash_filelike

from pyutils.images import get_image_dimensions


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
        parent_page_class = self.clean_parent_page_models()[0]
        parent_page = Page.objects.type(parent_page_class).first()
        _index_page = parent_page_class._meta.verbose_name.replace(" ", "").lower()
        index_page = getattr(parent_page, _index_page)
        try:
            index_page.add_child(instance=self)
        except NodeAlreadySaved:
            pass

    def save_revision(
        self,
        user=None,
        submitted_for_moderation=False,
        approved_go_live_at=None,
        changed=True,
        log_action=False,
        previous_revision=None,
        clean=True,
    ):
        if user:
            self.created_by = user
        return super(BasePage, self).save_revision(
            user,
            submitted_for_moderation,
            approved_go_live_at,
            changed,
            log_action,
            previous_revision,
            clean,
        )

    def save(self, clean=True, user=None, log_action=False, **kwargs):
        self.set_title()
        self.set_parent_page()
        super(BasePage, self).save(clean, user, log_action, **kwargs)

    class Meta:
        abstract = True


def child_has_parent(child):
    return child.depth and child.path


def save_uploaded_image(uploaded_file: InMemoryUploadedFile, filename=None):
    fn = filename or uploaded_file.name
    fp = f"media/original_images/{fn}"
    with open(fp, "wb") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)
    w, h = get_image_dimensions(fp)
    _hash = hash_filelike(open(fp, "rb"))
    image, _ = Image.objects.get_or_create(
        title=fn,
        file=f"original_images/{fn}",
        width=w,
        height=h,
        file_hash=_hash,
    )
    return image
