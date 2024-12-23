import phonenumbers
from phonenumbers import NumberParseException
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    """
    Validate a phone number for any country.
    """
    try:
        phone = phonenumbers.parse(value, region="GE")
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError("Invalid phone number.")
    except NumberParseException:
        raise ValidationError("Invalid phone number format.")
