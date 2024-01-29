import time
import logging
from datetime import timedelta

from django.test import TestCase, tag
from django.utils import timezone as tz
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from account.otp.helper.typings import PositiveInt, Minutes
from account.otp.models import OneTimePassword
from account.otp.helper import exceptions as exc
from account.otp.helper.text_choices import (
    OTPStateOptions,
    OTPReasonOptions,
    OTPTypeOptions
)

User = get_user_model()

class OneTimePasswordTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='+989123334444',
            password='test-password'
        )
        self.lifespan = Minutes(1)
        self.counter = 1
        self.DEFAULT_TOKEN_LENGTH = 4
        logging.disable(logging.CRITICAL)

    def test_totp_creation(self):
        totp = OneTimePassword.bll.create_totp(
            self.user,
            self.lifespan,
            OTPReasonOptions.REGISTRATION
        )
        self.assertIsNotNone(totp, msg="TOTP objects should not be None")
        self.assertEqual(len(totp.token), self.DEFAULT_TOKEN_LENGTH)
        self.assertEqual(totp.user, self.user, msg="User should match the provided user.")
        self.assertEqual(totp.reason, OTPReasonOptions.REGISTRATION, msg="Reason should match the provided reason")
        self.assertLessEqual(totp.expiry_time - tz.now(), timedelta(minutes=self.lifespan), msg="Expiry time should be approximately the provided duration.")

    def test_totp_creation_no_user(self):
        with self.assertRaises(exc.TokenError, msg="Token Error must be raised but it doesn't happen."):
            OneTimePassword.bll.create_totp(
                None,
                self.lifespan,
                OTPReasonOptions.REGISTRATION
            )

    def test_totp_creation_non_positive_lifespan(self):
        with self.assertRaises(exc.TokenLifeSpanError, msg="Token Error must be raised but it doesn't happen."):
            OneTimePassword.bll.create_totp(
                self.user,
                -1,
                OTPReasonOptions.REGISTRATION
            )
        with self.assertRaises(exc.TokenError):
            OneTimePassword.bll.create_totp(
                self.user,
                0,
                OTPReasonOptions.REGISTRATION
            )

    def test_totp_creation_invalid_max_retry(self):
        with self.assertRaises(RuntimeError):
            OneTimePassword.bll.create_totp(
                self.user,
                self.lifespan,
                OTPReasonOptions.REGISTRATION
            )

    def tearDown(self):
        logging.disable(logging.NOTSET)
        super().tearDown()
