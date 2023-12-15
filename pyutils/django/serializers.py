import pytz
from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.settings import api_settings

from pyutils.django.models import BaseModel


class LocalTimeStampField(serializers.DateTimeField):
    def __init__(self):
        super(LocalTimeStampField, self).__init__(
            read_only=True,
            format=api_settings.DATETIME_FORMAT,
            default_timezone=pytz.timezone(settings.LOCAL_TIME_ZONE),
        )


class GenericSerializer(ModelSerializer):
    class Meta:
        abstract = True
        read_only_fields = ["id", "created_at"]
        fields = "__all__"


class BaseModelSerializer(ModelSerializer):
    @property
    def model(self) -> type[BaseModel]:
        return getattr(self, "Meta").model


class IdModelSerializer(BaseModelSerializer):
    # def to_representation(self, instance):
    #     if isinstance(instance, int) and instance > 0:
    #         return self._get_object(instance)
    #     return super().to_representation(instance)

    def to_internal_value(self, data):
        if isinstance(data, int) and data > 0:
            return self._get_object_by_id(data)
        return super().to_internal_value(data)

    def _get_object_by_id(self, data_or_instance):
        try:
            return self.model.objects.get(id=data_or_instance)
        except self.model.DoesNotExist as e:
            raise e(
                "Could not find {} with id {}".format(
                    self.model.model_name_verbose, data_or_instance
                )
            )


class NameModelSerializer(BaseModelSerializer):
    """
    Serializer model instance with name
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and len(data) > 0:
            return self._get_object_by_name(data)
        return super().to_representation(data)

    def _get_object_by_name(self, data_or_instance):
        try:
            return self.model.objects.get(name=data_or_instance)
        except self.model.DoesNotExist as e:
            raise e(
                "Could not find {} with name {}".format(
                    self.model.model_name_verbose, data_or_instance
                )
            )


class NameIdModelSerializer(NameModelSerializer, IdModelSerializer):
    """
    Serializer model instance with name or id
    """

    def to_internal_value(self, data):
        instance = None
        try:
            instance = self._get_object_by_name(data_or_instance=data)
        except self.model.DoesNotExist:
            pass
        try:
            instance = self._get_object_by_id(data)
        except self.model.DoesNotExist:
            pass
        if instance is None:
            raise self.model.DoesNotExist(
                "Could not find {} with name or id {}".format(
                    self.model.model_name_verbose, data
                )
            )

    def _get_object_by_name(self, data_or_instance):
        try:
            return self.model.objects.get(name=data_or_instance)
        except self.model.DoesNotExist as e:
            raise e(
                "Could not find {} with name {}".format(
                    self.model.model_name_verbose, data_or_instance
                )
            )


class LocalTimeStampModelSerializer(BaseModelSerializer):
    created = LocalTimeStampField()
    modified = LocalTimeStampField()
