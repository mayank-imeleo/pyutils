from rest_framework.serializers import ModelSerializer


class GenericSerializer(ModelSerializer):
    class Meta:
        abstract = True
        read_only_fields = ["id", "created_at"]
        fields = "__all__"
