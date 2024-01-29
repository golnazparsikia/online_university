from django.db import models
from account.auth.models.user import User

class UserQueryset(models.QuerySet):

    @staticmethod
    def get_active_users():
        qs = User.objects.filter(is_active=True)
        return qs

    @staticmethod
    def get_superusers():
        qs = User.objects.filter(is_superuser=True)
        return qs

    @staticmethod
    def get_users_with_email():
        qs = User.objects.exclude(email__isnull=True)
        return qs

    @staticmethod
    def get_users_with_no_email():
        qs = User.objects.filter(email__isnull=True)
        return qs

    @staticmethod
    def get_users_with_first_name_starting_with(letter):
        qs = User.objects.filter(first_name__istartswith=letter)
        return qs

    @staticmethod
    def get_users_created_before(date):
        qs = User.objects.filter(created__lt=date)
        return qs
