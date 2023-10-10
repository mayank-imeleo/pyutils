from rest_framework.response import Response
from rest_framework.views import APIView

from pyutils.string import pascal_case_to_dash_case


class ModelFieldChoicesAPIView(APIView):
    """
    Viewset to provide all choice fields of a model
    """

    model = None

    def get_choice_mapping(self):
        fields = self.model._meta.fields
        choice_fields = []
        mapping = {}
        for field in fields:
            if getattr(field, "choices"):
                mapping[field.attname] = field.choices
        return mapping

    def get(self, *args, **kwargs):
        data = {"fields": self.get_choice_mapping()}
        return Response(data)

    @classmethod
    def url_prefix(cls) -> str:
        s = pascal_case_to_dash_case(cls.model.__name__)
        return f"{s}-field-choices/"
