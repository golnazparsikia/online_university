from django.db import models
from django.conf import settings
from django.core.validators import (
    MaxLengthValidator,
    MinLengthValidator,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


from painless.models.mixins.common import TimestampMixin
from account.otp.helper import (
    OTPStateOptions,
    OTPTypeOptions,
    OTPReasonOptions
)

from ..validators.text_choices import(
    OTPReasonOptionsValidator,
    OTPTypeOptionsValidator,
    OTPStateOptionsValidator
)

class OneTimePassword(TimestampMixin):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="user",
        related_name='tokens',
        on_delete=models.CASCADE,
        help_text="Token reserved for the specified user",
        db_comment="Token reserved for the specified user",
        db_index= True,
    )

    token = models.CharField(
        "Token",
        max_length=12,
        validators=[
            MaxLengthValidator(12),
            MinLengthValidator(4)
        ],
        db_comment = "the on-time password token (otp token) use for "\
                    "tow factor and multi factor authentication",

        help_text= "the on-time password token (otp token) use for "\
                    "tow factor and multi factor authentication",
        
        db_index=True,
    )

    expiry_time= models.DateTimeField(
        "expiry time",
        blank=True,
        null=True,
        help_text="the expiration time of the TOTP tokens ",
        db_comment= "the expiration time of the TOTP tokens",
    )

    counter = models.PositiveBigIntegerField(
        "counter",
        blank=True,
        null=True,
        help_text="the current counter value for HOTP tokens",
        db_comment= "the current counter value for HOTP tokens",
    )

    state= models.CharField(
        "state",
        max_length=10,
        choices=OTPStateOptions.choices ,
        validators=[OTPStateOptionsValidator()],
        help_text="the state of the token, whether it is consumed, expired or active",
        db_comment="the state of the token, whether it is consumed, expired or active"
    )

    type= models.CharField(
        max_length=10,
        choices=OTPTypeOptions.choices,
        validators=[OTPTypeOptionsValidator()],
        help_text="the type of token whether it os HOTP or TOTP",
        db_comment="the type of token whether it os HOTP or TOTP",
    )

    reason= models.CharField(
        "reason",
        max_length=40,
        choices=OTPReasonOptions.choices,
        validators=[OTPReasonOptionsValidator()],
        help_text="the reason of the token's creation. such as registration,"\
                    "password reset, email activation, or phonenumber activation",

        db_comment="the reason of the token's creation. such as registration,"\
                    "password reset, email activation, or phonenumber activation"
    )

    objects=models.Manager()
    
    class Meta:
        db_table ="account_otp_one_time_password",
        db_table_comment ="the one-time password table represent the creation"\
                        "creation of an otp token. wich is a on-time password"\
                            "that is used for security purposes",
        verbose_name="one time password",
        verbose_name_plural="one time passwords",
        default_manager_name="objects",

        constraints = [
            models.CheckConstraint(
                check=models.Q(expiry_time__gte =models.F('created')),
                name='expiry time created'
            ),

            models.UniqueConstraint(
                fields=['user', 'token', 'reason', 'type'],
                condition=models.Q(state__in=OTPStateOptions.ACTIVE),
                name='otp_uniqueness'
            ),
            models.CheckConstraint(
                check=models.Q(state__in=OTPStateOptions.values),
                name='otp_valid_state'
            ),
            models.CheckConstraint(
                check=models.Q(reason__in=OTPReasonOptions.values),
                name='otp_valid_reason'
            ),
            models.CheckConstraint(
                check=models.Q(type__in=OTPTypeOptions.values),
                name='otp_valid_type'
            ),
            models.CheckConstraint(
                check=(
                    models.Q(type=OTPTypeOptions.HOTP, counter_isnull=False, expiry_time_isnull=True),
                    models.Q(type=OTPTypeOptions.TOTP, counter_isnull=True, expiry_time_isnull=False)
                ),
            name= 'otp_counter_expiry_check'
            )
        ]
    def clean(self):
        existing_active_otps= self.__class__.objects.filter(
            user=self.user,
            token=self.token,
            reason=self.reason,
            type=self.type,
            state=OTPStateOptions.ACTIVE
        )

        if self.pk:
            existing_active_otps= existing_active_otps.exclude(pk=self.pk)

            if existing_active_otps.exists():
                raise ValidationError({
                    'duplicate_active_token': _ (
                        "another active OTP already exists for this user:"\
                        f"{self.user.username}, token: *****, type: {self.type}"\
                        f"and, reason: {self.reason}."
                    )
                })
            
        if self.type == OTPTypeOptions.HOTP and (self.counter is None):
            raise ValidationError(
                {
                    "hotp_counter": _(
                        "counter must be set for HOTP type and reason."
                        "Also, expiry time must be empty."
                    )
                }
            )
        
        if self.type == OTPTypeOptions.TOTP and (self.expiry_time is None):
            raise ValidationError(
                {
                    "totp_counter": _(
                        "expiry time must be set for tOTP type and reason."
                        "Also, counter must be empty."
                    )
                }
            )
        
        # ! TASK: State Design Pattern
        super().clean()

    def __str__(self) :
        return f"{self.user.username}: {self.token}"
    
    def __repr__(self) :
        return f"{self.user.username}: {self.token}"
    
class TimeBasedOneTimePassword(OneTimePassword):
    class Meta:
        proxy = True,
        verbose_name=_("time based one time password"),
        verbose_name_plural=_("time based one time password")

class HMACBasedOneTimePassword(OneTimePassword):
    class Meta:
        proxy = True,
        verbose_name=_("HMAC based one time password"),
        verbose_name_plural=_("HMAC based one time password")