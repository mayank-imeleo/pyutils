from typing import Type

import pendulum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import SearchFilter
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

    filter_backends = [DjangoFilterBackend, SearchFilter]

    @classmethod
    def model(cls) -> BaseModel:
        """
        Directly access the `Model` class
        """
        serializer_class = (
            cls.serializer_class or list(cls.action_serializer_classes.values())[0]
        )
        if not serializer_class:
            raise Exception(
                "You need to specify either"
                " serializer_class or action_serializer_classes"
            )
        return serializer_class.Meta.model

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

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class TimeStampedListModelMixin(mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        self._parse_date_fields(request, *args, **kwargs)
        return super().list(request, *args, **kwargs)

    def _parse_date_fields(self, request, *args, **kwargs):
        def parse(field):
            if field in request.query_params:
                dt = pendulum.parse(request.query_params[field])
                if field.endswith("__lte"):
                    dt = dt.add(days=1)  # add 1 day to include the end date
                request.query_params[field] = dt

        parse("created__date")
        parse("created__lte")
        parse("created__gte")


BaseModelViewSet = GenericModelViewSet


class GenericReadOnlyModelViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericModelViewSet
):
    pass


class GenericRetrieveModelViewSet(mixins.RetrieveModelMixin, GenericModelViewSet):
    @classmethod
    def url_prefix(cls) -> str:
        """
        "Some Model" => some-model-details
        :return:
        """
        s = getattr(cls.model(), "_meta").verbose_name.replace(" ", "")
        return pascal_case_to_dash_case(s) + "-details"


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


class ViewSetActionSerializerMixin:
    """
    Mixin to use action serializers for a viewset.
    """

    action_serializer_classes = {
        "list": None,
        "create": None,
        "destroy": None,
        "retrieve": None,
        "update": None,
    }

    def create(self, request, *args, **kwargs):
        """
        Use retrieve serializer for serializing the created instance.
        """
        response = super().create(request, *args, **kwargs)
        assert "id" in response.data, "id not found in response"
        retreive_serializer_class = self.action_serializer_classes["retrieve"]
        model_class = self.model()
        instance = model_class.objects.get(id=response.data["id"])
        retreive_data = retreive_serializer_class(instance).data
        response.data = retreive_data
        return response

    def get_serializer_class(self):
        """
        Look for serializer class in self.serializer_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(ViewSetMultipleSerializerMixin, ViewSet):
            serializer_classes = {
                'list': MyListSerializer,
                'my_action': MyActionSerializer,
            }
        """
        try:
            return self.action_serializer_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()
