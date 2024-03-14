from django.contrib import admin


class BaseDjangoAdmin(admin.ModelAdmin):
    """
    Base Django Admin
    """

    list_display = (
        "id",
        "name",
    )
    search_fields = ["name"]
    ordering = ("id",)


class BaseModelAdmin(admin.ModelAdmin):
    class Media:
        js = ["admin/js/jquery.init.js", "pyutils/js/django/listFilters.js"]


class TimeStampedModelAdmin(BaseModelAdmin):
    """
    Base Django Admin
    """

    list_display = (
        "created",
        "modified",
    )
    search_fields = ()
    ordering = ("-modified",)


TimeStampedAdmin = TimeStampedModelAdmin


class UserTimeStampedModelAdmin(BaseModelAdmin):
    """
    Base Django Admin
    """

    def save_model(self, request, obj, form, change):
        try:
            obj.created_by
        except AttributeError:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


UserTimeStampedAdmin = UserTimeStampedModelAdmin


class ReadOnlyAdmin(BaseModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
