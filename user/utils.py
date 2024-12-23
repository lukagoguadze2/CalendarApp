import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_number


def get_country_code(phone_number: str, default_region: str = "GE"):
    try:
        # Parse the phone number
        parsed_number = phonenumbers.parse(phone_number, default_region)

        # Get the country code
        country_code = parsed_number.country_code

        # Get the region code (optional)
        region = region_code_for_number(parsed_number)

        return {
            "country_code": country_code,
            "region": region
        }
    except phonenumbers.NumberParseException:
        return None
