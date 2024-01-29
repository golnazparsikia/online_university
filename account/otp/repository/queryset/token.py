from django.db import models
from django.contrib.auth import get_user_model

from account.otp.helper.text_choices import (
    OTPStateOptions,
    OTPReasonOptions,
    OTPTypeOptions
)

User = get_user_model()

class OTPQuerySet(models.QuerySet):

    def filter_actives(self):
        qs = self.filter(state=OTPStateOptions.ACTIVE)
        return qs

    def filter_consumes(self):
        qs = self.filter(state=OTPStateOptions.CONSUME)
        return qs

    def filter_expired(self):
        qs = self.filter(state=OTPStateOptions.EXPIRE)
        return qs

    def filter_by_user(self, user: User):
        qs = self.select_related('user').filter(user=user)
        return qs

    def filter_by_reason(self, reason: OTPReasonOptions):
        qs =  self.filter(reason=reason)
        return qs

    def filter_by_type(self, otp_type: OTPTypeOptions):
        qs = self.filter(type=otp_type)
        return qs

    def created_before(self, timestamp):
        qs = self.filter(created__lt=timestamp)
        return qs

    def created_after(self, timestamp):
        qs = self.filter(created__gt=timestamp)
        return qs

    def add_total_active_state(self):
        qs = self.annotate(
            total_active_states=models.Count(
                models.Q(
                    state__iexact=OTPStateOptions.ACTIVE.value
                )
            )
        )
        return qs
