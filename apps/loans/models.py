# Third Party
from django.db import models

# App
from apps.users.models import User
from miniAspire.currencies import Currency
from miniAspire.models import BaseModel


class Loan(BaseModel):
    class LoanStatus(models.TextChoices):
        PENDING = "PENDING"
        APPROVED = "APPROVED"
        PAID = "PAID"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.INR.value
    )
    term = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=LoanStatus.choices,
        default=LoanStatus.PENDING.value,
    )

    def __str__(self):
        return f"Loan-{self.user}-{self.amount}-{self.id}"


class Repayment(BaseModel):
    class RepaymentStatus(models.TextChoices):
        PENDING = "PENDING"
        PAID = "PAID"

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="repayments")
    repayment_date = models.DateField()
    paid_on = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=RepaymentStatus.choices,
        default=RepaymentStatus.PENDING.value,
    )

    def __str__(self):
        return f"Repayment-{self.loan}-{self.id}"

