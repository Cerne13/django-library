# Generated by Django 4.1 on 2022-11-30 15:35

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("borrowings", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("PENDING", "PENDING"), ("FAILED", "FAILED")],
                        default="PENDING",
                        max_length=50,
                    ),
                ),
                (
                    "payment_type",
                    models.CharField(
                        choices=[("PAYMENT", "PAYMENT"), ("FINE", "FINE")],
                        default="PAYMENT",
                        max_length=50,
                    ),
                ),
                ("session_url", models.CharField(max_length=200)),
                ("session_id", models.CharField(max_length=50)),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[
                            django.core.validators.MinValueValidator(Decimal("0.01"))
                        ],
                    ),
                ),
                (
                    "borrowing_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="borrowings.borrowing",
                    ),
                ),
            ],
        ),
    ]