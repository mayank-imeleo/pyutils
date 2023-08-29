from typing import Type

from rest_framework import mixins
from rest_framework.routers import SimpleRouter
from rest_framework.viewsets import GenericViewSet

from pyutils.django.models import BaseModel
from pyutils.string import pascal_case_to_dash_case


class GenericModelViewSet(GenericViewSet):
    """
    A subclass of `GenericViewSet` with some additional `Model` specific
    methods that would make working with the `Model` more seamless.

    Mixins can be added while inheriting from the class to offer CRUD features.

    See the respective methods for more documentation:
    """

    @classmethod
    def model(cls) -> BaseModel:
        """
        Directly access the `Model` class
        """
        return cls.serializer_class.Meta.model

    @classmethod
    def url_prefix(cls) -> str:
        """
        Returns verbose_name_plural in dash-case.

        It is used as `prefix` while registering a `ViewSet` with a `Router`.

        So now you do not have to use raw strings while adding a `ViewSet` to
        a router. Simply, use this method to specify the `verbose-name-plural`
        as the `prefix`.

        For eg, instead of:
        router.register(prefix='disclosure-sub-categories',viewset=DisclosureSubCategoryViewSet)

        you can do:
        router.register(
            prefix=DisclosureSubCategoryViewSet.url_prefix(),
            viewset=DisclosureSubCategoryViewSet)

        Now the model is available at the url:
        <host>/api/<path>/disclosure-sub-categories/{id}

        In case you change the `verbose-name-plural` in the future, changes
        will get automatically get reflected
        in the URL path as well.
        """
        s = getattr(cls.model(), "_meta").verbose_name_plural
        s = s.replace(" ", "")
        return pascal_case_to_dash_case(s)


class GenericReadOnlyModelViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericModelViewSet
):
    pass


class GenericCRUDModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericModelViewSet,
):
    pass


def router_register_viewset(router: SimpleRouter, viewset: Type[GenericModelViewSet]):
    """
    register the router with the given viewset
    """
    router.register(viewset.url_prefix(), viewset)
    return router
