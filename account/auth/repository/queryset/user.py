from django.apps import apps
from django.db.models import(
    QuerySet,
    Q,
    F
)

class UserQuerySet(QuerySet):

    def filter_active_users(self, is_active=True):
        qs = self.filter(self, is_active=is_active)
        return qs
    
    def filter_normal_users(self, is_active=True):
        qs= self.filter_active_users(is_active=is_active).filter(
            Q(is_superuser=False) & 
            Q(is_staff=False)
        )
        return qs
    
    def filter_super_users(self, is_active=True):
        qs= self.filter_active_users(is_active=is_active).filter(
            Q(is_superuser=True) & 
            Q(is_staff=True)
        )
        return qs
    
    def filter_staff_users(self, is_active=True):
        qs= self.filter_active_users(is_active=is_active).filter(
            Q(is_superuser=False) & 
            Q(is_staff=True)
        )
        return qs
    