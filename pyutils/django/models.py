# from python_utils import formatters
from boltons.strutils import camel2under
from django.db import models
from django.db.models import base
from django.template import defaultfilters
from model_utils import models as mu_models

from pyutils.string import pascal_case_to_dash_case, pascal_case_to_underscore_case


class ModelBaseMeta(base.ModelBase):
    """
    Model base with more readable naming convention

    Example:
    Assuming the model is called `app.FooBarObject`

    Default Django table name: `app_foobarobject`
    Table name with this base: `app_foo_bar_object`
    """

    def __new__(cls, name, bases, attrs):
        module = attrs["__module__"]

        # Get or create Meta
        if "Meta" in attrs:
            Meta = attrs["Meta"]
        else:
            Meta = type(
                "Meta",
                (object,),
                dict(
                    __module__=module,
                ),
            )
            attrs["Meta"] = Meta

        # Override table name only if not explicitly defined
        if not hasattr(Meta, "db_table"):  # pragma: no cover
            module_name = camel2under(name)
            app_label = module.split(".")[-2]
            Meta.db_table = f"{app_label}_{module_name}"

        return base.ModelBase.__new__(cls, name, bases, attrs)


class ModelNameMixin:
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
    def model_name_upper_case(cls):
        """
        underscore_case verbose_name

        Verbose Name => verbose_name
        """
        return pascal_case_to_underscore_case(cls._meta.verbose_name.replace(" ", ""))

    @classmethod
    @property
    def model_name_plural_upper_case(cls):
        """
        underscore_case verbose_name_plural

        Verbose Name Plurals => verbose_name_plurals
        """
        return pascal_case_to_underscore_case(
            cls._meta.verbose_name_plural.replace(" ", "")
        )


class UUIDModel(mu_models.UUIDModel, ModelNameMixin):
    """
    Abstract base model for all models.

    Adds UUID primary key, created_at, and updated_at fields.
    """

    class Meta:
        abstract = True


class CreatedAtModelBase(mu_models.TimeStampedModel, ModelNameMixin):
    updated_at = models.DateTimeField(verbose_name="Updated At", auto_now=True)
    created_at = models.DateTimeField(verbose_name="Created At", auto_now_add=True)

    class Meta:
        abstract = True


TimeStampedModel = CreatedAtModelBase


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


class SlugMixin(NameMixin):
    """Mixin to automatically slugify the name and add both a name and slug to
    the model

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

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = defaultfilters.slugify(self.name)

        super(NameMixin, self).save(*args, **kwargs)

    class Meta(object):
        unique_together = ("slug",)


class NameModelBase(models.Model, ModelNameMixin):
    name = models.CharField(verbose_name="Name", max_length=100)

    class Meta:
        abstract = True


NameModel = NameModelBase


class SlugModelBase(SlugMixin, NameModelBase):
    slug = models.SlugField(max_length=50)

    class Meta:
        abstract = True


SlugModel = SlugModelBase


class NameCreatedAtModelBase(NameModel, mu_models.TimeStampedModel):
    class Meta:
        abstract = True


NameTimeStampedModel = NameCreatedAtModelBase


class SlugCreatedAtModelBase(SlugModel, mu_models.TimeStampedModel):
    class Meta:
        abstract = True


SlugTimeStampedModel = SlugCreatedAtModelBase
