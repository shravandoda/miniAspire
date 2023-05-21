# Third Party
from django.contrib import admin

from apps.loans.models import Loan, Repayment


def mark_as_approved(model_admin, request, queryset):
    for item in queryset:
        item.status = Loan.LoanStatus.APPROVED.value
        item.save()


def mark_as_paid(model_admin, request, queryset):
    for item in queryset:
        item.status = Loan.LoanStatus.PAID.value
        item.save()


class LoanAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "amount",
        "amount_paid",
        "currency",
        "term",
        "status",
        "created_at",
    ]
    list_filter = [
        "status",
    ]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
    ]
    raw_id_fields = [
        "user",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    actions = [
        mark_as_paid,
        mark_as_approved,
    ]


def mark_as_paid(model_admin, request, queryset):
    for item in queryset:
        item.status = Repayment.RepaymentStatus.PAID.value
        item.save()


class RepaymentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "loan",
        "amount",
        "amount_paid",
        "repayment_date",
        "status",
        "created_at",
    ]
    list_filter = [
        "status",
    ]
    search_fields = [
        "loan__user__username",
        "loan__user__first_name",
        "loan__user__last_name",
    ]
    raw_id_fields = [
        "loan",
    ]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    actions = [
        mark_as_paid,
    ]


admin.site.register(Loan, LoanAdmin)
admin.site.register(Repayment, RepaymentAdmin)
