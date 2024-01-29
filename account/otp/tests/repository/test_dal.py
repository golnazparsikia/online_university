from datetime import timedelta

from django.test import TestCase
from django.utils import timezone as tz
from django.contrib.auth import get_user_model

from account.otp.models import OneTimePassword
from account.otp.helper.text_choices import (
    OTPStateOptions,
    OTPTypeOptions,
    OTPReasonOptions
)


User = get_user_model()

class TestOTPQuerySet(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            phone_number='+989123334444',
            password='pass1'
        )

        OneTimePassword.objects.create(
            user=self.user1,
            token='123456',
            expiry_time=tz.now() + timedelta(minutes=1),  # Assuming a 10-minute expiry time
            state=OTPStateOptions.ACTIVE.value,
            type=OTPTypeOptions.TOTP.value,
            reason=OTPReasonOptions.REGISTRATION.value
        )

        OneTimePassword.objects.create(
            user=self.user1,
            token='123456',
            expiry_time=tz.now() + timedelta(minutes=1),  # Assuming a 10-minute expiry time
            state=OTPStateOptions.EXPIRE.value,
            type=OTPTypeOptions.TOTP.value,
            reason=OTPReasonOptions.REGISTRATION.value
        )

    def test_add_total_active_states(self):
        otp_obj = OneTimePassword.dal.add_total_active_states() \
                                .filter(state=OTPStateOptions.ACTIVE.value) \
                                .filter(user=self.user1) \
                                .first()
        actual = otp_obj.total_active_states
        expected = 1
        self.assertEqual(actual, expected)
