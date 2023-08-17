import email.utils as eutils
import re

from unidecode import unidecode


def validate_email(contact_value) -> str:
    try:
        normalized_email = unidecode(contact_value.lower())
        pattern = r"^[a-zA-Z0-9@]*$"
        sanitized_email = re.sub(pattern, "", normalized_email)
        sanitized_email.strip()
        parsed_email = eutils.parseaddr(sanitized_email)
        if not parsed_email[1]:
            raise ValueError("Invalid email format")
        domain = parsed_email[1].split("@")[1]
        if not re.match(r"^[a-zA-Z0-9.-]+$", domain):
            raise ValueError("Invalid email format")

        return sanitized_email
    except Exception:
        raise ValueError("Invalid email format")


def validate_portuguese_phone(contact_value) -> str:
    try:
        sanitized_contact_value = str(re.sub(r"\D", "", contact_value))
        if not sanitized_contact_value.startswith("2") and not re.match(r"^\d{9}$", str(sanitized_contact_value)):
            raise ValueError("Phone number must be a 9-digit number and start with 2")
        return contact_value
    except Exception:
        raise ValueError("Invalid phone")


def validate_portuguese_mobile(contact_value) -> str:
    try:
        sanitized_contact_value = str(re.sub(r"\D", "", contact_value))
        if not sanitized_contact_value.startswith("9") and not re.match(r"^\d{9}$", str(sanitized_contact_value)):
            raise ValueError("Mobile number must be a 9-digit number and start with 9")
        return contact_value
    except Exception:
        raise ValueError("Invalid mobile")


def validate_contact_value(value, self) -> str:
    if self.contact_type == "email":
        return validate_email(value)
    if self.organization.vat_country == "PT":
        if self.contact_type == "phone":
            return validate_portuguese_phone(value)
        elif self.contact_type == "mobile":
            return validate_portuguese_mobile(value)
        else:
            raise ValueError("Invalid contact type")
    elif self.contact_type == "phone" or self.contact_type == "mobile":
        return value
    else:
        raise ValueError("Invalid contact type")
