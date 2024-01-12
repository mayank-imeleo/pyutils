import pendulum

from pyutils.django.viewsets import GenericModelViewSet


class DateRangeFilterViewsetMixin(GenericModelViewSet):
    def filter_queryset(self, queryset):
        end_date_key = "created__lte"
        if end_date_key in self.request.query_params:
            dt = pendulum.parse(self.request.query_params[end_date_key])
            # add 1 day to include the end date
            self.request.query_params[end_date_key] = dt.add(days=1).to_date_string()
        return super().filter_queryset(queryset)
