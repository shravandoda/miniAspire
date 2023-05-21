# Third Party
from django.db import transaction
from rest_framework import serializers

# App
from apps.loans.models import Loan, Repayment
from miniAspire.currencies import Currency


class LoanCreateSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(required=True, allow_null=False)
    term = serializers.IntegerField(required=True, allow_null=False)
    currency = serializers.ChoiceField(
        choices=Currency.choices, required=True, allow_null=False
    )

    class Meta:
        model = Loan
        fields = ["id", "amount", "currency", "term", "status"]
        extra_kwargs = {
            "id": {"read_only": True},
        }

    def validate_amount(self, amount):
        if not amount:
            raise serializers.ValidationError("Amount cannot be null or 0")
        return amount

    def validate_term(self, term):
        if not term:
            raise serializers.ValidationError(
                "Term cannot be null and has to be atleast 1"
            )
        return term


class LoanApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["status"]


class LoanDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ["id", "amount", "currency", "term", "status"]


class RepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repayment
        fields = ["id", "loan", "repayment_date", "amount", "status"]


class RepaymentUpdateSerializer(serializers.ModelSerializer):
    payment = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)

    class Meta:
        model = Repayment
        fields = ["payment"]

    def validate_payment(self, value):
        remaining_loan_amount = (
            self.instance.loan.amount - self.instance.loan.amount_paid
        )
        if value > remaining_loan_amount:
            raise serializers.ValidationError(
                "The payment cannot exceed the remaining loan amount."
            )
        if value < self.instance.amount - self.instance.amount_paid:
            raise serializers.ValidationError(
                "The payment must be greater than or equal to the unpaid balance."
            )
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        payment = validated_data.get("payment")

        pending_repayments = Repayment.objects.filter(
            loan=instance.loan, status=Repayment.RepaymentStatus.PENDING.value
        ).order_by("repayment_date")

        for repayment in pending_repayments:
            if payment <= 0:
                break
            if payment >= repayment.amount - repayment.amount_paid:
                remaining_amount = repayment.amount - repayment.amount_paid
                repayment.amount_paid = repayment.amount
                repayment.status = Repayment.RepaymentStatus.PAID.value
                payment -= remaining_amount
            else:
                repayment.amount_paid += payment
                payment = 0

            repayment.save()

        return instance

    def to_representation(self, instance):
        instance.refresh_from_db()
        return RepaymentSerializer(instance).data
