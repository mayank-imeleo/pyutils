"""
Django Utils
"""
import abc
import logging
from typing import Dict, Tuple

import jwt
from django.conf import settings
from django.db import models
from django.db.models import Model
from django.template.defaultfilters import truncatechars
from jsonpath_ng import parse

from .string import pascal_case_to_dash_case, pascal_case_to_underscore_case

logger = logging.getLogger(__name__)
LOCAL = "local"


class BaseModel(models.Model):
    """
    Base Django Model
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def fc_name(cls):
        """
        flatcase verbose_name
        `TargetSection` => `targetsections`
        """
        return cls._meta.verbose_name.lower().replace(" ", "")  # pylint: disable[E1101]

    @classmethod
    def dc_name(cls):
        """
        dash-case verbose-name
        Verbose Name=> verbose-name
        """
        return pascal_case_to_dash_case(cls._meta.verbose_name.replace(" ", ""))

    @classmethod
    def dc_name_plural(cls):
        """
        dash-case verbose_name_plural
        Verbose Name Plurals => verbose-name-plurals
        """
        return pascal_case_to_dash_case(cls._meta.verbose_name_plural.replace(" ", ""))

    @classmethod
    def uc_name(cls):
        """
        underscore_case verbose_name

        Verbose Name => verbose_name
        """
        return pascal_case_to_underscore_case(cls._meta.verbose_name.replace(" ", ""))

    @classmethod
    def uc_name_plural(cls):
        """
        underscore_case verbose_name_plural

        Verbose Name Plurals => verbose_name_plurals
        """
        return pascal_case_to_underscore_case(cls._meta.verbose_name_plural.replace(" ", ""))


def text_ellipsis(text: str):
    return truncatechars(text, settings.ADMIN_CMS["ELLIPSES_LENGTH"])


def is_aws_available():
    if not (settings.AWS_ACCESS_KEY_ID and not settings.AWS_SECRET_ACCESS_KEY):
        return False


def is_env_local():
    return settings.ENVIRONMENT == LOCAL


def aws_skip_test() -> Tuple[bool, str]:
    skip = not is_aws_available()
    if skip:
        return skip, "AWS credentials not available"
    return skip, "AWS credentials  available"


def skip_test_in_local():
    """
    Skip a test if SKIP_TEST_IN_LOCAL=True in .env
    Returns:

    """
    return settings.SKIP_TEST_IN_LOCAL


def jwt_token(payload: dict) -> str:
    """
    Return a JWT token for authentication
    Args:
        payload (dict): The payload for the JWT token
    Returns:
    """
    secret_key = settings.SECRET_KEY
    logger.critical("JWT Token SECRET_KEY: %s", secret_key)
    return jwt.encode(payload, key=secret_key, algorithm="HS256")


SKIP_TEST_LOCAL_MSG = "SKIP_TEST_IN_LOCAL set to True .env"


def update_model_from_dict(model_obj: Model, data: Dict):
    for key, value in data.items():
        setattr(model_obj, key, value)
    model_obj.save()


class ModelDataMapper(abc.ABC):
    model: Model = None
    field_mapping = {}  # ('field_name','proc_func')
    json_paths = []

    def __init__(self, data: Dict):
        self.model_obj = None
        self.data = data
        self.rows = []
        if self.json_paths:
            for json_path in self.json_paths:
                jsonpath_expr = parse(json_path)
                data_list = [match.value for match in jsonpath_expr.find(data)]
                if not isinstance(data_list, list):
                    raise ValueError("json_path should return a list")
                for item in data_list[0]:
                    item["_json_path"] = json_path
                self.rows.extend(data_list[0])
        else:
            self.rows = [
                data,
            ]

        self.updated_data = {}

    def update_model_kwargs(self, kwargs):
        """
        Update the model kwargs
        """
        return kwargs

    def load_model_obj(self, kwargs):
        """
        Load the model object
        """
        self.model_obj, _ = self.model.objects.get_or_create(**kwargs)

    def update(self):
        """
        Update the mapping
        """
        if not self.is_applicable():
            return
        for row in self.rows:
            self._update(row)

    def _update(self, row):
        self.updated_data = self.get_updated_data_dict(row, self.field_mapping)
        kwargs = self.update_model_kwargs(self.updated_data)
        self.load_model_obj(kwargs)
        self.after_update()
        self.model_obj.save()

    def after_update(self):
        """
        Use this as a hook.
        :return:
        """
        return

    @staticmethod
    def get_updated_data_dict(data: Dict, field_mapping: Dict):
        """
        Get the updated data dictionary
        """
        updated_data = {}
        for key, val in data.items():
            if key not in field_mapping:
                continue
            field_name, proc_func = field_mapping.get(key)
            target_val = val
            if proc_func:
                target_val = proc_func(val)
            updated_data.setdefault(field_name, target_val)
        return updated_data

    def is_applicable(self):
        """
        If tests is applicable
        """
        return True
