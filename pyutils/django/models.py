import uuid

# from python_utils import formatters
from boltons.strutils import camel2under
from django.db import models
from django.db.models import base
from django.template import defaultfilters

from pyutils.string import pascal_case_to_dash_case, pascal_case_to_underscore_case


class ModelBaseMeta(base.ModelBase):
    '''
    Model base with more readable naming convention

    Example:
    Assuming the model is called `app.FooBarObject`

    Default Django table name: `app_foobarobject`
    Table name with this base: `app_foo_bar_object`
    '''

    def __new__(cls, name, bases, attrs):
        module = attrs['__module__']

        # Get or create Meta
        if 'Meta' in attrs:
            Meta = attrs['Meta']
        else:
            Meta = type(
                'Meta', (object,), dict(
                    __module__=module,
                )
            )
            attrs['Meta'] = Meta

        # Override table name only if not explicitly defined
        if not hasattr(Meta, 'db_table'):  # pragma: no cover
            module_name = camel2under(name)
            app_label = module.split('.')[-2]
            Meta.db_table = f'{app_label}_{module_name}'

        return base.ModelBase.__new__(cls, name, bases, attrs)


class ModelBase(models.Model, metaclass=ModelBaseMeta):
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
        return pascal_case_to_underscore_case(cls._meta.verbose_name_plural.replace(" ", ""))

    class Meta:
        abstract = True


class UUIDBaseModel(ModelBase):
    """
    Abstract base model for all models.

    Adds UUID primary key, created_at, and updated_at fields.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class CreatedAtModelBase(ModelBase):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class NameMixin(object):
    '''Mixin to automatically get a unicode and repr string base on the name

    >>> x = NameMixin()
    >>> x.pk = 123
    >>> x.name = 'test'
    >>> repr(x)
    '<NameMixin[123]: test>'
    >>> str(x)
    'test'
    >>> str(str(x))
    'test'

    '''

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return f'<{self.__class__.__name__}[{self.pk or -1:d}]: {self.name}>'


class SlugMixin(NameMixin):
    '''Mixin to automatically slugify the name and add both a name and slug to
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

    '''

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = defaultfilters.slugify(self.name)

        super(NameMixin, self).save(*args, **kwargs)

    class Meta(object):
        unique_together = ('slug',)


class NameModelBase(NameMixin, ModelBase):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class SlugModelBase(SlugMixin, NameModelBase):
    slug = models.SlugField(max_length=50)

    class Meta:
        abstract = True


class NameCreatedAtModelBase(NameModelBase, CreatedAtModelBase):
    class Meta:
        abstract = True


class SlugCreatedAtModelBase(SlugModelBase, CreatedAtModelBase):
    class Meta:
        abstract = True
