# Third Party
from rest_framework import generics
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

# App
from apps.loans.models import Loan, Repayment
from apps.loans.permissions import IsSuperUserOrReadOnly, NonSuperuserPermission
from apps.loans.serializers import (
    LoanApproveSerializer,
    LoanCreateSerializer,
    LoanDetailsSerializer,
    RepaymentUpdateSerializer,
)


class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanDetailsSerializer
    permission_classes = [IsAuthenticated, NonSuperuserPermission]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.serializer_class = LoanCreateSerializer
        return super(LoanListCreateView, self).create(request, *args, **kwargs)


class LoanApproveView(generics.UpdateAPIView):
    queryset = Loan.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "id"
    serializer_class = LoanApproveSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(status=Loan.LoanStatus.APPROVED.value)


class LoanRetrieveView(generics.RetrieveUpdateAPIView):
    queryset = Loan.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "id"
    serializer_class = LoanDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class RepaymentUpdateView(generics.UpdateAPIView):
    serializer_class = RepaymentUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        loan_id = self.kwargs.get("loan_id")
        loan = Loan.objects.filter(id=loan_id, user=self.request.user).first()

        if not loan:
            raise NotFound("No such loan found for this user.")

        if loan.status == Loan.LoanStatus.PAID.value:
            raise PermissionDenied("The loan is already paid.")

        if loan.status == Loan.LoanStatus.PENDING.value:
            raise PermissionDenied("The loan is yet to be approved.")

        repayment = (
            Repayment.objects.filter(loan=loan, status="PENDING")
            .order_by("repayment_date")
            .first()
        )

        if not repayment:
            raise NotFound("No pending repayments found for this loan.")

        return repayment
