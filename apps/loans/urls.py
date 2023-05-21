# Third Party
from django.urls import path

# App
from apps.loans.views import (
    LoanApproveView,
    LoanListCreateView,
    LoanRetrieveView,
    RepaymentUpdateView,
)

urlpatterns = [
    path("", LoanListCreateView.as_view(), name="loan_list"),
    path(
        "<int:loan_id>/repayment/",
        RepaymentUpdateView.as_view(),
        name="repayment_update",
    ),
    path("<int:id>/", LoanRetrieveView.as_view(), name="loan_details"),
    path("approve/<int:id>/", LoanApproveView.as_view(), name="loan_approve"),
]
