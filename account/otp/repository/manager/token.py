from django.db import models
from django.contrib.auth import get_user_model

from ..queryset import OTPQuerySet

from account.otp.helper.text_choices import (
    OTPStateOptions,
    OTPReasonOptions,
    OTPTypeOptions
)

User = get_user_model()

class OTPDataAccessLayer(models.Manager):
    def get_query_set(self):
        return OTPQuerySet(self.model, using=self._db)

    def filter_actives(self):
        return self.get_query_set().filter_actives()

    def filter_consumes(self):
        return self.get_query_set().filter_consumes()

    def filter_expired(self):
        return self.get_query_set().filter_expires

    def filter_by_user(self, user: User):
        return self.get_query_set().filter_by_user(user)

    def filter_by_reason(self, reason: OTPReasonOptions):
        return self.get_query_set().filter_by_reason(reason)

    def filter_by_type(self, otp_type: OTPTypeOptions):
        return self.get_query_set().filter_by_type(otp_type)

    def created_before(self, timestamp):
        return self.get_query_set().created_before(timestamp)

    def created_after(self, timestamp):
        return self.get_query_set().created_after(timestamp)

    def add_total_active_state(self):
        return self.get_query_set().add_total_active_state()
