from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as DjangoUserManager, AbstractUser
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from pyutils.django.models import NameAddressTimeStampedModel


class UserManager(DjangoUserManager):
    """Custom manager for the User model."""

    def _create_user(self, email: str, password: str | None, **extra_fields):
        """
        - normalize the email
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def get_superuser(self):
        return self.filter(is_superuser=True).order_by("id").first()

    def get_admin_user(self):
        """
        Return the first user with the Admin group.
        """
        return self.filter(groups__name="Admin").order_by("id").first()

    def get_system_user(self):
        """
        Return the system user.
        """
        return self.get(email=settings.SYSTEM_USER_EMAIL)


class AbstractEmailUser(NameAddressTimeStampedModel, AbstractUser):
    """
    Base user with email as username. And with other fields such as
    name, address, phone_number, created_by, modified_by etc
    """

    first_name = CharField(_("First Name"), blank=True, max_length=255)
    last_name = CharField(_("Last Name"), blank=True, max_length=255)
    objects = UserManager()
    email = EmailField(_("email address"), unique=True)

    def __str__(self):
        return "{} {} ({})".format(self.first_name, self.last_name, self.email)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    @property
    def group_names(self):
        return [str(g) for g in self.groups.all()]

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["name"]
