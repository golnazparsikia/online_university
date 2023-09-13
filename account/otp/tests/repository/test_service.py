import logging
from unittest.mock import patch, Mock

from django.test import TestCase
from django.contrib.auth import get_user_model

from account.otp.helper import exceptions as exc
from account.otp.repository.service import OTPService

User = get_user_model()


class TestGenerateTokenTOTP(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            phone_number="+989123334444",
            password="test-password"
        )
        self.token_length = 6
        self.lifespan = 1
        logging.disable(logging.CRITICAL)

    @patch('pyotp.TOTP')
    def test_generate_totp_token_success(self, mock_totp):
        mock_totp_instance = mock_totp.return_value
        mock_totp_instance.now.return_value = '123456'  

        result = OTPService.generate_token_totp(
            self.user,
            self.token_length,
            self.lifespan
        )

        self.assertEqual(result, '123456')

    def test_generate_totp_token_invalid_user_failure(self):
        user = None

        with self.assertRaises(exc.TokenError):
            OTPService.generate_token_totp(
                user,
                self.token_length,
                self.lifespan
            )

    def tearDown(self):
        logging.disable(logging.NOTSET)
        super().tearDown()
