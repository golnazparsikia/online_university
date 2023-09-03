
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from ..helper.text_choices import (
    OTPReasonOptions,
    OTPStateOptions,
    OTPTypeOptions
)

@deconstructible
class OTPReasonOptionsValidator:
    def __call__(self, value: str) -> None:
        valid_choices = [choice[0] for choice in OTPReasonOptions.choices]
        if value not in valid_choices:
            raise ValidationError(
                _("%(value)s is not a valid reason option"),
                params ={"value": value}
            )
        

@deconstructible
class OTPStateOptionsValidator:
    def __call__(self, value: str) -> None:
        valid_choices = [choice[0] for choice in OTPStateOptions.choices]
        if value not in valid_choices:
            raise ValidationError(
                _("%(value)s is not a valid state option"),
                params ={"value": value}
            )
        

@deconstructible
class OTPTypeOptionsValidator:
    def __call__(self, value: str) -> None:
        valid_choices = [choice[0] for choice in OTPTypeOptions.choices]
        if value not in valid_choices:
            raise ValidationError(
                _("%(value)s is not a valid Type option"),
                params ={"value": value}
            )