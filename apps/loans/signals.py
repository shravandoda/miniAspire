# Third Party
from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# App
from apps.loans.models import Loan, Repayment


@receiver(post_save, sender=Loan)
def create_repayment(sender, instance, created, **kwargs):
    if created:
        for i in range(instance.term):
            if i < instance.term - 1:
                amount = Decimal(instance.amount) / Decimal(instance.term)
            else:
                # Calculate the remaining amount for the last repayment
                amount = Decimal(instance.amount) - (
                    Repayment.objects.filter(loan=instance).aggregate(
                        models.Sum("amount")
                    )["amount__sum"]
                    or 0
                )
            Repayment.objects.create(
                repayment_date=timezone.now().date() + timezone.timedelta(weeks=i + 1),
                amount=amount,
                loan=instance,
                status="PENDING",
            )


@receiver(post_save, sender=Repayment)
def update_loan_amount_paid(sender, instance, **kwargs):
    loan = instance.loan
    total_paid = (
        Repayment.objects.filter(loan=loan).aggregate(total=models.Sum("amount_paid"))[
            "total"
        ]
        or 0
    )
    loan.amount_paid = total_paid
    if loan.amount_paid >= loan.amount:
        loan.status = Loan.LoanStatus.PAID.value
    loan.save()
