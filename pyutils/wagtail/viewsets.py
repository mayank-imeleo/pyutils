from typing import Union

from rest_framework import mixins, status
from rest_framework.response import Response
from treebeard.exceptions import NodeAlreadySaved
from wagtail.models import Page

from pyutils.django.viewsets import GenericModelViewSet
from pyutils.wagtail.models import PageAutoFieldsMixin


class PageCRUDViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericModelViewSet,
):
    index_page_model: Page
    child_page_model: Union[Page, PageAutoFieldsMixin]
    child_page_instance: Union[Page, PageAutoFieldsMixin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        self.after_perform_create(request, *args, **kwargs)
        headers = self.get_success_headers(self.response_data(serializer))
        return Response(
            self.response_data(serializer),
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def response_data(self, serializer):
        data = serializer.data
        data["id"] = getattr(self.child_page_instance, "id")
        return data

    def perform_create(self, serializer):
        return self.add_child(**serializer.validated_data)

    def after_perform_create(self, request, *args, **kwargs):
        """
        Hook to update the created instance
        """
        pass

    def add_child(self, **kwargs):
        if not (
            getattr(self, "index_page_model", None)
            and getattr(self, "child_page_model", None)
        ):
            raise AttributeError(
                f"index_page_model or child_page_model"
                f" is not defined for {self.__class__.__name__}"
            )
        index_page = Page.objects.type(self.index_page_model).first()
        child_page: PageAutoFieldsMixin = self.child_page_model(**kwargs)
        child_page.title = child_page.auto_title
        child_page.slug = child_page.auto_slug

        try:
            self.child_page_instance = index_page.add_child(instance=child_page)
        except NodeAlreadySaved:
            self.child_page_instance = child_page
