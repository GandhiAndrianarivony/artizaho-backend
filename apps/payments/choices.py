from api.utils import Enumeration


class PaymentStatus(Enumeration):
    PAID = "Paid"
    IN_PROGRESS = "InProgress"
    NOT_PAID = "Not Paid"
