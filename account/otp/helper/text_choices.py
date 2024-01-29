from django.db import models


class OTPStateOptions(models.TextChoices):
    CONSUME = ('consume', 'Consume')
    EXPIRE = ('expire', 'Expire')
    ACTIVE = ('active', 'Active')


class OTPTypeOptions(models.TextChoices):
    HOTP = ('hopt', 'Hotp')
    TOTP = ('totp', 'Totp')


class OTPReasonOptions(models.TextChoices):
    REGISTRATION = ('registration', 'Registration')
    LOGIN = ('login', 'Login')
    RESET_PASSWORD = ('reset_password', 'Reset Password')
    EMAIL_ACTIVATION = ('email_activation', 'Email Activation')
    PHONE_NuMBER_ACTIVATION = ('phone_number_activation', 'Phone Number Activation')
    PAYMENT = ('payment', 'Payment')
    TWO_STEP_VERIFICATION = ('tow_step_verification', 'Two Step Verification')
