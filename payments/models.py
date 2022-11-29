from django.db import models


class Payment(models.Model):
    status = models.CharField(
        max_length=50, choices=(
            ("PENDING", "PENDING"), ("FAILED", "FAILED")
        ), default="PENDING"
    )
    payment_type = models.CharField(
        max_length=50, choices=(
            ("PAYMENT", "PAYMENT"), ("FINE", "FINE")
        ), default="PAYMENT"
    )
    borrowing_id = models.AutoField(primary_key=True)
    session_url = models.CharField(max_length=200)
    session_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.status
