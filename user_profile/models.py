from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not phone_number:
            raise ValueError('The given email must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        """Create user"""

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """Create and save a SuperUser with the given phone_number and password."""

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    """Create custom user"""

    username = None
    phone_number = PhoneNumberField(_('phone_number'), unique=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)


class UserProfile(models.Model):
    """Create User profile"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_referral_code = models.CharField(max_length=6, default=get_random_string(length=6))
    activated_referral_code = models.CharField(max_length=6, null=True, default=None)
    reg_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """Save method to make sure that we have unique referral code"""

        code = self.user_referral_code
        while UserProfile.objects.filter(user_referral_code=code).exclude(pk=self.pk).exists():
            code = get_random_string(length=6)
        self.user_referral_code = code
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user.phone_number)