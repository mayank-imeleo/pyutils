"""
Utils for factory_boy.
https://github.com/FactoryBoy/factory_boy
"""
import factory
from factory import Faker
from factory.django import DjangoModelFactory


class FieldFaker(Faker):
    def refresh(self):
        """
        Returns a new value
        """
        return self._get_faker().format(self.provider)


class WordFaker(Faker):
    """
    A single word
    """

    def __init__(self, **kwargs):
        super().__init__(provider="words", **kwargs)


class ModelNameFaker(Faker):
    """
    Two words in Title Case
    Eg:
    Nothing Learn
    Trouble Rise
    Bar Poor
    """

    def __init__(self, **kwargs):
        super().__init__(provider="words", nb=2, **kwargs)

    def evaluate(self, instance, step, extra):
        s = " ".join(super().evaluate(instance, step, extra))
        return s.title()


class SentenceFaker(Faker):
    """
    A fake sentence.
    """

    def __init__(self, **kwargs):
        super().__init__(provider="sentence", **kwargs)


ModelDescriptionFaker = SentenceFaker


class ParagraphFaker(Faker):
    """
    A fake paragraph.
    """

    def __init__(self, **kwargs):
        super().__init__(provider="paragraph", **kwargs)


class BooleanFaker(Faker):
    """
    A fake boolean.
    """

    def __init__(self, **kwargs):
        super().__init__(provider="pybool", **kwargs)


class IntFaker(Faker):
    """
    A random integer
    """

    def __init__(self, **kwargs):
        super().__init__(provider="random_int", **kwargs)


class CompanyNameFaker(Faker):
    """
    A fake company name.
    Eg:
    Johnson-Murphy
    Cunningham, Harris and Chen
    Vasquez Inc
    """

    def __init__(self, **kwargs):
        super().__init__(provider="company", **kwargs)


class EmailFaker(Faker):
    """
    A fake email address
    Eg:
    fbrown@example.net
    zacharysanders@example.net
    """

    def __init__(self, **kwargs):
        super().__init__(provider="email", **kwargs)


class UrlFaker(Faker):
    """
    A fake url.
    Eg:
    http://fitzgerald.org/
    https://www.mckenzie.com/
    """

    def __init__(self, **kwargs):
        super().__init__(provider="url", **kwargs)


class ImageFilePathFaker(Faker):
    """
    A fake image file path.
    Eg:
    /lot/miss.jpeg
    /research/those.jpeg
    """

    def __init__(self, **kwargs):
        super().__init__(provider="file_path", category="image", extension="jpeg")


class ForeignKeyFaker(factory.SubFactory):
    """
    A fake foreign key object.
    """

    def __init__(self, parent_factory: type[DjangoModelFactory], **kwargs):
        super(ForeignKeyFaker, self).__init__(factory=parent_factory, **kwargs)
