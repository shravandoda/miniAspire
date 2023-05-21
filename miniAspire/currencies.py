# Third Party
from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class Currency(TextChoices):
    AED = "AED", _("AED")
    AUD = "AUD", _("AUD")
    BRL = "BRL", _("BRL")
    CAD = "CAD", _("CAD")
    EUR = "EUR", _("EUR")
    GBP = "GBP", _("GBP")
    IDR = "IDR", _("IDR")
    INR = "INR", _("INR")
    SGD = "SGD", _("SGD")
    THB = "THB", _("THB")
    USD = "USD", _("USD")

    @classmethod
    def get_symbol(cls, currency):
        symbol = ""
        if currency == cls.AED.value:
            symbol = "د.إ"
        elif currency == cls.AUD.value:
            symbol = "A$"
        elif currency == cls.BRL.value:
            symbol = "R$"
        elif currency == cls.CAD.value:
            symbol = "C$"
        elif currency == cls.EUR.value:
            symbol = "€"
        elif currency == cls.GBP.value:
            symbol = "£"
        elif currency == cls.IDR.value:
            symbol = "Rp"
        elif currency == cls.INR.value:
            symbol = "₹"
        elif currency == cls.SGD.value:
            symbol = "S$"
        elif currency == cls.THB.value:
            symbol = "฿"
        elif currency == cls.USD.value:
            symbol = "$"
        return symbol
