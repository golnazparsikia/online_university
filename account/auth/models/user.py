import uuid

import phonenumbers

from django.utils.translation import gettext_lazy as _

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
    
    
)

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.validators import validate_international_phonenumber

from ..repository.manager import UserManager
from painless.models.mixins.common import TimestampMixin
from ..validators import IRPhoneNumberValidator 

class User(AbstractUser, TimestampMixin):
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS=[]

    username = models.CharField(
        _("Username"),
        max_length=14,
        unique= True,
        help_text= "_",
        error_messages={
            "unique ": "this number is already exists"
        }
    )

    phone_number = PhoneNumberField(
        _("phone number"),
        unique= True,
        validators=[IRPhoneNumberValidator()],
        region="IR",
        error_messages={
            "unique" : "this number is already exists",
        }
    )

    secret_code = models.UUIDField(
        _("secret code"),
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text=""
    )
    
    email = models.EmailField(
        _("email Address"),
        unique= False,
        null= True,
        blank=False
    )

    objects =UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural ="Users"
        default_manager_name = "objects"

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username