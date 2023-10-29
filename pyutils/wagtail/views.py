from wagtail.images.components import ImageDisplay
from wagtail.snippets.views.snippets import InspectView

from pyutils.django.models import BaseModel


class ModelInspectView(InspectView):
    page_title = f"Details - "

    def get_fields_context(self):
        fields_context = []
        for field_name in self.fields:
            field_context = self.get_context_for_field(field_name)
            if (
                isinstance(field_context["value"], ImageDisplay)
                and not field_context["value"].value
            ):
                continue
            fields_context.append(field_context)
        return fields_context
