"""
Pydantic models for the account holders API response.
Describes the data structure: account holders, email addresses, postal addresses, and phones.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, model_validator


class Name(BaseModel):
    """Account holder's full name."""

    first: str
    last: str
    middle: Optional[str] = None
    suffix: Optional[str] = None

    @field_validator("first", "last")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        """First and last name must not be empty strings."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("Name cannot be empty")
        return stripped

    @property
    def full_name(self) -> str:
        """Returns full name as a single string."""
        parts = [self.first]
        if self.middle:
            parts.append(self.middle)
        parts.append(self.last)
        if self.suffix:
            parts.append(self.suffix)
        return " ".join(parts)


class Holder(BaseModel):
    """Account holder: relationship type and name."""

    relationship: str
    name: Name


class Address(BaseModel):
    """Postal address."""

    type: str
    line1: str
    line2: Optional[str] = None
    city: str
    region: str
    postalCode: str
    country: str

    @field_validator("postalCode")
    @classmethod
    def postal_code_not_empty(cls, value: str) -> str:
        """Postal code must not be empty."""
        if not value.strip():
            raise ValueError("Postal code cannot be empty")
        return value

    @field_validator("country")
    @classmethod
    def country_code_length(cls, value: str) -> str:
        """Country code must be 2 characters (ISO 3166-1 alpha-2)."""
        if len(value.strip()) != 2:
            raise ValueError("Country code must be two letters (ISO 3166-1 alpha-2)")
        return value.upper()


class Telephone(BaseModel):
    """Phone number with country code."""

    type: str
    country: str
    number: str

    @field_validator("number")
    @classmethod
    def number_digits_only(cls, value: str) -> str:
        """Phone number must contain digits only."""
        if not value.isdigit():
            raise ValueError(f"Phone number must contain digits only, got: '{value}'")
        return value

    @field_validator("country")
    @classmethod
    def country_code_digits_only(cls, value: str) -> str:
        """Country calling code must contain digits only."""
        if not value.isdigit():
            raise ValueError(f"Country code must contain digits only, got: '{value}'")
        return value

    @property
    def full_number(self) -> str:
        """Returns full number in format +<country_code><number>."""
        return f"+{self.country}{self.number}"


class AccountHoldersResponse(BaseModel):
    """
    Root API response model.
    Contains account holders, email addresses, postal addresses, and phones.
    """

    holders: list[Holder]
    emails: list[EmailStr]
    addresses: list[Address]
    telephones: list[Telephone]

    @model_validator(mode="after")
    def must_have_primary_holder(self) -> "AccountHoldersResponse":
        """Response must contain at least one primary holder (PRIMARY or PRIMARY_JOINT)."""
        primary_types = {"PRIMARY", "PRIMARY_JOINT"}
        has_primary = any(h.relationship in primary_types for h in self.holders)
        if not has_primary:
            raise ValueError("holders list must contain at least one PRIMARY or PRIMARY_JOINT holder")
        return self

    @model_validator(mode="after")
    def holders_and_emails_count_match(self) -> "AccountHoldersResponse":
        """Number of email addresses must match number of holders."""
        if len(self.emails) != len(self.holders):
            raise ValueError(
                f"Email count ({len(self.emails)}) "
                f"does not match holders count ({len(self.holders)})"
            )
        return self