from django.shortcuts import redirect
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

import stripe

from .models import Payment
from .serializers import (
    PaymentSerializer,
)


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset

        if not self.request.user.is_staff:
            return queryset.filter(user=self.request.user)

        return queryset


# class CreateCheckoutSession(APIView):
#     def post(self, request):
#         dataDict = dict(request.data)
#         price = 1
#         product_name = "product_name"
#         try:
#             checkout_session = stripe.checkout.Session.create(
#                 line_items=[{
#                     "price_data": {
#                         "currency": "usd",
#                         "product_data": {
#                             "name": product_name,
#                         },
#                         "unit_amount": price
#                     },
#                     "quantity": 1
#                 }],
#                 mode="payment",
#                 checkout_s=checkout_session.id,
#                 checkout_u=checkout_session.url
#                 # success_url=FRONTEND_CHECKOUT_SUCCESS_URL,
#                 # cancel_url=FRONTEND_CHECKOUT_FAILED_URL,
#             )
#             # return redirect(checkout_session.url, code=303)
#         except Exception as e:
#             print(e)
#             return e
