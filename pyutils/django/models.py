# from python_utils import formatters

from cities_light.models import Country, Region, SubRegion
from django.conf import settings
from django.db import models
from model_utils import models as mu_models
from smart_selects.db_fields import ChainedForeignKey

from pyutils.django.managers import TimeStampedModelManager
from pyutils.string import pascal_case_to_dash_case, pascal_case_to_underscore_case

SubRegion.__str__ = lambda x: x.name
Region.__str__ = lambda x: x.name
Country.__str__ = lambda x: x.name


class IdMixin(object):
    def __repr__(self):
        return "{}(id={})".format(self.__class__.__name__, getattr(self, "id"))

    __str__ = __repr__


class NameMixin(object):
    """Mixin to automatically get a unicode and repr string base on the name

    >>> x = NameMixin()
    >>> x.pk = 123
    >>> x.name = 'test'
    >>> repr(x)
    '<NameMixin[123]: test>'
    >>> str(x)
    'test'
    >>> str(str(x))
    'test'

    """

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return f"<{self.__class__.__name__}[{self.pk or -1:d}]: {self.name}>"


class BaseModel(models.Model, IdMixin):
    @classmethod
    @property
    def model_name_verbose(cls):
        return cls._meta.verbose_name

    @classmethod
    @property
    def model_name_verbose_plural(cls):
        return cls._meta.verbose_name_plural

    @classmethod
    @property
    def model_name_flat_case(cls):
        """
        flatcase verbose_name
        `TargetSection` => `targetsections`
        """
        return cls._meta.verbose_name.lower().replace(" ", "")  # pylint: disable[E1101]

    @classmethod
    @property
    def model_name_dash_case(cls):
        """
        dash-case verbose-name
        Verbose Name=> verbose-name
        """
        return pascal_case_to_dash_case(cls._meta.verbose_name.replace(" ", ""))

    @classmethod
    @property
    def model_name_plural_dash_case(cls):
        """
        dash-case verbose_name_plural
        Verbose Name Plurals => verbose-name-plurals
        """
        return pascal_case_to_dash_case(cls._meta.verbose_name_plural.replace(" ", ""))

    @classmethod
    @property
    def model_name_underscore_case(cls):
        """
        underscore_case verbose_name

        Verbose Name => verbose_name
        """
        return pascal_case_to_underscore_case(cls._meta.verbose_name.replace(" ", ""))

    @classmethod
    @property
    def model_name_plural_underscore_case(cls):
        """
        underscore_case verbose_name_plural

        Verbose Name Plurals => verbose_name_plurals
        """
        return pascal_case_to_underscore_case(
            cls._meta.verbose_name_plural.replace(" ", "")
        )

    class Meta:
        abstract = True


class NameModel(NameMixin, BaseModel):
    name = models.CharField(verbose_name="Name", max_length=100, unique=True)

    class Meta:
        abstract = True


class UserStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_by`` and ``modified_by`` fields.

    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_createdby_relationship",
        blank=True,
        null=True,
        default=None,
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(app_label)s_%(class)s_modifiedby_relationship",
        blank=True,
        null=True,
        default=None,
    )

    def _save_user_stamps(self, *args, **kwargs):
        # self.modified_by = self.get_
        update_fields = kwargs.get("update_fields", None)
        if update_fields:
            kwargs["update_fields"] = set(update_fields).union({"modified"})

        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class TimeStampedModel(mu_models.TimeStampedModel, BaseModel):
    objects = TimeStampedModelManager

    def _save_time_stamps(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields", None)
        if update_fields:
            kwargs["update_fields"] = set(update_fields).union({"modified"})

    class Meta:
        abstract = True


class NameAddressTimeStampedModel(NameModel, TimeStampedModel):
    add_line_1 = models.CharField(
        "Address Line 1", max_length=200, default="", blank=True, null=True
    )
    add_line_2 = models.CharField(
        "Address Line 2", max_length=200, default="", blank=True, null=True
    )
    phone_num = models.CharField(
        "Phone Number", max_length=20, default="", blank=True, null=True
    )

    email_address = models.EmailField(
        "Email Address", max_length=20, default="", blank=True, null=True
    )

    city = ChainedForeignKey(
        SubRegion,
        chained_field="state",
        chained_model_field="region",
        auto_choose=True,
        on_delete=models.SET_NULL,
        null=True,
    )
    state = ChainedForeignKey(
        Region,
        chained_field="country",
        chained_model_field="country",
        auto_choose=True,
        on_delete=models.SET_NULL,
        null=True,
    )
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    pincode = models.CharField(max_length=6, default="", blank=True, null=True)

    class Meta:
        abstract = True


class NameTimeStampedModel(NameModel, TimeStampedModel):
    class Meta:
        abstract = True


class UserTimeStampedModel(UserStampedModel, TimeStampedModel):
    def save(self, *args, **kwargs):
        self._save_user_stamps(*args, **kwargs)
        self._save_time_stamps(*args, **kwargs)

    class Meta:
        abstract = True
