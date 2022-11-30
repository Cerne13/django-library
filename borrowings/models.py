from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import ForeignKey, CheckConstraint, Q, F
from django.db.models.functions import Now
from rest_framework.exceptions import ValidationError

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = ForeignKey(
        Book, on_delete=models.CASCADE,
        related_name="borrowings"
    )
    user = ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="borrowings"
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(
                    borrow_date__lte=Now()),
                name="check_borrowing_date"
            ),
            CheckConstraint(
                check=Q(expected_return_date__gt=Now()),
                name="check_expected_return_date",
            ),
            CheckConstraint(
                check=Q(expected_return_date__gte=F("borrow_date")),
                name="check_expected_return_is_after_borrow",
            ),
            CheckConstraint(
                check=Q(
                    actual_return_date__gte=Now()
                ),
                name="check_return_date"
            ),
        ]

    # To validate in admin panel also
    @staticmethod
    def validate_book_available(inventory_avail, err_type):
        if not inventory_avail:
            raise err_type("Sorry, we are out of such books.")

    def clean(self):
        Borrowing.validate_book_available(self.book.inventory, ValidationError)

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )
