import inspect
import os
import random
from pathlib import Path
from typing import Type

from django.conf import settings
from django.core.management import call_command
from django.db import models
from django.db.models import BooleanField, Model
from django.test import TestCase, TransactionTestCase
from factory.django import DjangoModelFactory


class IsActiveModelTestCaseMixin:
    def test_is_active(self):
        _object = getattr(self, "object")
        is_active: BooleanField = getattr(_object, "is_active")
        assert isinstance(is_active, BooleanField)


class ModelBaseFactory(DjangoModelFactory):
    pass


class ModelBaseTestCaseMixin:
    model_class: Type[models.Model]

    @classmethod
    def _check_model_class(cls, model_class: Type[models.Model]):
        if isinstance(cls.model_class, models.Model):
            raise TypeError(
                f"model_class must be of type {models.Model}. Not its instance"
            )
        elif not isinstance(cls.model_class, type(models.Manager)):
            raise TypeError(
                "model_class must be of type {models.Model}. Got: %s"
                % type(cls.model_class)
            )

    @property
    def count(self):
        return self.model_class.objects.count()

    @classmethod
    def _parent_fp(cls) -> Path:
        return Path(inspect.getfile(cls)).parent

    @classmethod
    def _sibling_fp(cls, fn: str) -> Path:
        return cls._parent_fp().joinpath(fn)


class ModelBaseTestCase(TestCase, ModelBaseTestCaseMixin):
    """
    Base class for all model test cases.
    """

    model_class: Type[models.Model]

    def __new__(cls, *args, **kwargs):
        cls._check_model_class(cls.model_class)
        return super().__new__(cls)


class ModelBaseTransactionTestCase(TransactionTestCase, ModelBaseTestCaseMixin):
    """
    Base class for all model test cases.
    """

    model_class: Type[models.Model]

    def __new__(cls, *args, **kwargs):
        cls._check_model_class(cls.model_class)
        return super().__new__(cls)


class ManagerBaseTestCase(TestCase):
    """
    Base class for all model manager test cases.
    """

    manager: models.Manager

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.manager, models.Manager):
            raise TypeError(f"manager must be an instance of {models.Manager} class.")
        return super().__new__(cls)


class ModelFactoryTestCaseMixin:
    model_class: Type[models.Model]
    model_factory: DjangoModelFactory
    count: int
    DUMP_FIXTURE = "factory_dump.yaml"
    INDENT_SPACES = 2

    @classmethod
    def _create(cls) -> Model:
        return cls.model_factory.create()

    @classmethod
    def _dumpdata(cls):
        # @formatter:off

        """
        Creates a YAML file as per the following command:

        ./manage.py dumpdata content.ModelName \
            --format yaml --indent 2 \
            --output tests/caravel_cmpas/<app_name>/<model_name>/factory_dump.yaml
        """
        # @formatter:on
        app_label = getattr(cls.model_class, "_meta").app_label
        model_name = cls.model_class.__name__
        model_path = f"{app_label}.{model_name}"
        kwargs = {
            "format": "yaml",
            "indent": cls.INDENT_SPACES,
            "output": cls._sibling_fp(fn=cls.DUMP_FIXTURE).__str__(),
        }
        call_command("dumpdata", model_path, **kwargs)

    def test_create_delete(self):
        n = self.count
        instance = self._create()
        assert n + 1 == self.count
        self._dumpdata()
        instance.delete()
        assert n == self.count


class ModelFixtureTestCaseMixin:
    model: Model
    is_fixture_created: bool

    def test_is_fixture_created(self):
        assert self.is_fixture_created, "fixtures were not created"


class ModelFactoryBaseTestCase(ModelBaseTestCase):
    """
    Base class for all model factory test cases.
    """

    model_factory: DjangoModelFactory
    model_class: Type[Model]
    model_instance: Model

    def __new__(cls, *args):
        cls.model_class = cls.model_factory._meta.model
        return super(ModelFactoryBaseTestCase, cls).__new__(cls)


class ModelFixtureBaseTestCase(ModelBaseTestCase):
    """
    Base class for all Model fixture test cases.
    """

    DEV_FIXTURE = "test_fixture_dev.yaml"
    BIZ_FIXTURE = "test_fixture_biz.yaml"
    is_fixture_created = False

    @classmethod
    def setUpClass(cls):
        fixtures = [
            cls.BIZ_FIXTURE,
        ]
        if os.path.exists(cls._sibling_fp("test_fixture_dev.yaml")):
            # test_fixture_dev.yaml are ignored in VCS
            # Test them only if they are present
            fixtures.append(cls.DEV_FIXTURE)
        fixtures_ = map(lambda fx: cls._sibling_fp(fx), fixtures)
        cls.fixtures = list(map(str, fixtures_))
        super(ModelFixtureBaseTestCase, cls).setUpClass()
        cls.is_fixture_created = True


def get_single_random_object_from_model(model_class: Type[Model]):
    """
    Returns a random object from a given model
    Args:
        model_class (Model): Model for which from return random objects
    """

    return _get_random_objects_from_model(model_class, n=1)


def get_multiple_random_objects_from_model(model_class: Type[Model], n: int = 1):
    """
    Returns a random object from a given model
    Args:
        n (int): Number of objects to return
        model_class (Model): Model for which from return random objects
    """
    return _get_random_objects_from_model(model_class, n)


def _get_random_objects_from_model(model_class: Type[Model], n: int = 1):
    if not n > 0:
        raise ValueError("n must be greater than 0")

    objects = list(model_class.objects.all())

    if n == 1:
        return random.choice(objects)
    else:
        return random.sample(objects, n)


def skip_test_in_ci():
    return {"condition": settings.SKIP_TEST_IN_CI, "reason": "Test disabled in CI"}


def skip_test_in_local():
    return {
        "condition": settings.SKIP_TEST_IN_LOCAL,
        "reason": "Test disabled in local",
    }
