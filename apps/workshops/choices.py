"""Module for all related workshop choices"""

from enum import Enum
from api.utils import Enumeration


class CurrencyType(Enumeration):
    DOLLARS = "USD"
    EURO = "EUR"


class CustomWorkshopStatus(Enumeration):
    VALID = 'Valid'
    REJECTED = 'Rejected'
    PENDING = 'Pending'
    NEW = "New"
