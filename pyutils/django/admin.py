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
