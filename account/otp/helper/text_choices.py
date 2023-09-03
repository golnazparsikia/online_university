from django.db import models

class OTPStateOptions(models.TextChoices):
    CONSUME =("consume", "consume")
    EXPIRE =("expire", "expire")
    ACTIVE =("active", "active")


class OTPTypeOptions(models.TextChoices):
    HOTP =("hotp", "hotp")
    TOTP=("totp", "totp")


class OTPReasonOptions(models.TextChoices):
    REGISTRATION = ("registration", "registration")
    LOGIN =("login", "login")
    RESET_PASSWORD =("reset_password", "reset_password")
    EMAIL_ACTIVATION =("email_activation", "email_activation")
    PHONE_NUMBER_ACTIVATION =("phone_number_activation", "phone_number_activation")
    PAYMENT=("payment", "payment")
    TOW_STEP_VERIFICATION =("tow_step_verification", "tow_step_verification")