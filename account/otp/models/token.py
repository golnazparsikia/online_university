from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
)
from django.core.exceptions import ValidationError

from painless.models.mixins.common import TimestampMixin

from account.otp.validators.text_choices import(
    OTPReasonOptionsValidator,
    OTPStateOptionsValidator,
    OTPTypeOptionsValidator,
)
from account.otp.helper.text_choices import(
    OTPReasonOptions,
    OTPStateOptions,
    OTPTypeOptions,
)
from ..repository.manager import OTPDataAccessLayer

class OneTimePassword(TimestampMixin):
    """
    Thr OneTimePassword model represents the creation of an OTP token.
    Which is a one-time password that is used for security purposes.
    such as:
        - two-factor authentication
        - multi-factor authentication

    This model keeps track of the token's creation and expiration time,
    and the reason and status of its creation.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="User",
        on_delete=models.CASCADE,
        related_name='tokens',
        help_text="Token Reserved for the specified user.",
        db_comment= "Token Reserved for the specified user.",
        db_index=True
    )

    token = models.CharField(
        "Token",
        max_length=12,
        validators=[
            MinLengthValidator(4),
            MaxLengthValidator(12)
        ],
        db_comment="The one-time password token (OTP token) use for "
                    "two-factor and multi-factor authentication.",
        help_text="The one-time password token (OTP token) use for "
                    "two-factor and multi-factor authentication.",
        db_index=True
    )

    expiry_time = models.DateTimeField(
        "Expiry Time",
        blank=True,
        null=True,
        help_text="The expiration time of the OTP tokens.",
        db_comment="The expiration time of the OTP tokens."
    )

    counter = models.PositiveSmallIntegerField(
        "Counter",
        blank=True,
        null=True,
        help_text="The current counter value for HTOP tokens.",
        db_comment="The current counter value for HOTP tokens."
    )

    reason = models.CharField(
        "Reason",
        max_length=40,
        choices=OTPReasonOptions.choices,
        validators=[OTPReasonOptionsValidator()],
        help_text="The reason for the token's creation."
                    " Such as registration, password reset, email activations"
                    " or phone number activation.",
        db_comment="The reason for the token's creation."
                    " Such as registration, password reset, email activations"
                    " or phone number activation."
    )

    state = models.CharField(
        "State",
        max_length=10,
        choices=OTPStateOptions.choices,
        validators=[OTPStateOptionsValidator()],
        help_text="The state of the token, whether it is consumed, expired "
                    "or active.",
        db_comment="The state of the token, whether it is consumed, expired "
                    "or active."
    )

    type = models.CharField(
        "Type",
        max_length=10,
        choices=OTPTypeOptions.choices,
        validators=[OTPTypeOptionsValidator()],
        help_text="The Type of the token whether it is a TOTP or HOTP",
        db_comment="The Type of the token whether it is a TOTP or HOTP"
    )

    objects = models.Manager()
    dal = OTPDataAccessLayer()

    class Meta:
        db_table = "account_otp_one_time_password"
        db_table_comment = "The One Time Password Table represents the " \
                            "creation of an OTP token. Which is a one-time " \
                            "password that is used for security purposes."
        verbose_name = "One Time Password"
        verbose_name_plural = "One Time Passwords"
        default_manager_name = "objects"

        constraints = [
            models.CheckConstraint(
                check=models.Q(expiry_time__gte=models.F('created')),
                name='expiry_time_gte_created',
            ),
            models.UniqueConstraint(
                fields=['user', 'token', 'reason', 'type'],
                condition=models.Q(state__in=OTPStateOptions.ACTIVE),
                name='otp_uniqueness'
            ),
            models.CheckConstraint(
                check=models.Q(reason__in=OTPReasonOptions.values),
                name='otp_valid_reason'
            ),
            models.CheckConstraint(
                check=models.Q(state__in=OTPStateOptions.values),
                name='otp_valid_state'
            ),
            models.CheckConstraint(
                check=models.Q(type__in=OTPTypeOptions.values),
                name='otp_valid_type'
            ),
            models.CheckConstraint(
                check=(
                    models.Q(
                        type=OTPTypeOptions.HOTP,
                        counter__isnull=False,
                        expiry_time__isnull=True
                    ) |
                    models.Q(
                        type=OTPTypeOptions.TOTP,
                        counter__isnull=True,
                        expiry_time__isnull=False
                    )
                ),
                name='otp_expiry_counter_check'
            )
        ]

    def clean(self) -> None:
        existing_active_otps = self.__class__.objects.filter(
            user=self.user,
            token=self.token,
            reason=self.reason,
            type=self.type,
            state=OTPStateOptions.ACTIVE
        )
        if self.pk:
            existing_active_otps = existing_active_otps.exclude(pk=self.pk)
            if existing_active_otps:
                raise ValidationError(
                    {
                    'duplicate_active_token': _(
                        "Another active OTP already exists for this user: "
                        f"{self.user.username}, token: ****, type: {self.type}"
                        f" and reason: {self.reason}"
                    )
                    }
                )

        if self.type == OTPTypeOptions.HOTP and self.counter is None:
            raise ValidationError(
                {
                    "hotp_counter":_(
                        "Counter must be set for HOTP and reason.",
                        "Also, expiry time must be empty."
                    )
                }
            )

        if self.type == OTPTypeOptions.TOTP and self.expiry_time is None:
            raise ValidationError(
                {
                    "totp_counter":_(
                        "Expiry time must be set for TOTP and reason.",
                        "Also, counter must be empty."
                    )
                }
            )

        # ! task: design pattern
        return super().clean()

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return super().__repr__()

class TimeBasedOneTimePassword(OneTimePassword):
    class meta:
        proxy = True,
        verbose_name = _("Time Based One Time Password")
        verbose_name_plural = _("Time Based One Time Passwords")


class HMACBasedOneTimePassword(OneTimePassword):
    class meta:
        proxy = True,
        verbose_name = _("HMAC Based One Time Password")
        verbose_name_plural = _("HMAC Based One Time Passwords")