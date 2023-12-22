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


class TimeStampedModelAdmin(admin.ModelAdmin):
    """
    Base Django Admin
    """

    list_display = (
        "created",
        "modified",
    )
    search_fields = ()
    ordering = ("-modified",)


class UserTimeStampedModelAdmin(admin.ModelAdmin):
    """
    Base Django Admin
    """

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
