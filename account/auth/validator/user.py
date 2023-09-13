from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible

@deconstructible
class IRPhoneNumberValidator(RegexValidator):
    regex = r'^\+98\d{10}$'
    message = "Enter a valid Iranian phone number with the format: '+98[9-digit number]'."
    code = "invalid_iranian_phone_number"