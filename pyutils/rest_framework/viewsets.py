import pendulum
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins
from wagtail.api.v2.filters import SearchFilter

from pyutils.django.viewsets import GenericModelViewSet
from pyutils.rest_framework.serializers import UserSerializer

User = get_user_model()


class DateRangeFilterViewsetMixin(GenericModelViewSet):
    def filter_queryset(self, queryset):
        end_date_key = "created__lte"
        if end_date_key in self.request.query_params:
            dt = pendulum.parse(self.request.query_params[end_date_key])
            # add 1 day to include the end date
            self.request.query_params[end_date_key] = dt.add(days=1).to_date_string()
        return super().filter_queryset(queryset)


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericModelViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = UserAdmin.search_fields
    filterset_fields = ["email", "id"]

    def filter_queryset(self, queryset):
        email = self.request.query_params.get("email")
        if email:
            return queryset.filter(email__iexact=email)
        return super().filter_queryset(queryset)
