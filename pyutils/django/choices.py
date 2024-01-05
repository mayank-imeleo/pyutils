from django.db.models import TextChoices


class BaseTextChoices(TextChoices):
    @classmethod
    def label_to_value(cls, label):
        for value_, label_ in cls.choices:
            if label_ == label:
                return value_

    @classmethod
    def value_to_label(cls, value):
        for value_, label_ in cls.choices:
            if value_ == value:
                return label_
