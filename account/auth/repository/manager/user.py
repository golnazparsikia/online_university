from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import BaseUserManager


from account.auth.repository.queryset import UserQuerySet

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number: str, password: str, **extra_fields):
        user = self.model(username=phone_number, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, phone_number: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)
    def create_superuser(self, phone_number: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValidationError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValidationError("Superuser must have is_superuser=True")
        return self._create_user(phone_number, password, **extra_fields)

    def create_staff(self, phone_number: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        if extra_fields.get('is_staff') is not True:
            raise ValidationError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is True:
            raise ValidationError("Superuser must have is_superuser=False")
        return self._create_user(phone_number, password, **extra_fields)

    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)