from django.urls import path, include
from rest_framework import routers

from payments.views import (
    PaymentViewSet,
    # CreateCheckoutSession
)

router = routers.DefaultRouter()
router.register("", PaymentViewSet)
# router.register("checkout", CreateCheckoutSession)


urlpatterns = [
    path("", include(router.urls)),
    # path("checkout/", CreateCheckoutSession.as_view(), name="checkout")
]

app_name = "payments"
