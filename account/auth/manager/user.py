from django.db import models
from account.auth.queryset.user import UserQueryset

class UserDAL(models.Manager):
    def get_query_set(self):
        qs = UserQueryset(self.model, using=self._db)
        return qs
    def filter_by_last_login(self, last_login):
        qs = self.get_query_set().filter(last_login=last_login)
        return qs
    def filter_by_is_staff(self, is_staff=True):
        qs = self.get_query_set().filter(is_staff=is_staff)
        return qs
    def filter_by_is_active_and_is_staff(self):
        qs = self.get_query_set().filter(is_active=True, is_staff=True)
        return qs
    def filter_by_full_name(self, full_name):
        qs = self.get_query_set().filter(models.Q(first_name__icontains=full_name) | models.Q(last_name__icontains=full_name))
        return qs