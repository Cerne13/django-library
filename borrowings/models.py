from django.db import models
from django.db.models import ForeignKey


# TODO: Add foreign keys to books, users
# TODO: constraints for borrow_date, expected_return_date, and actual_return_date.


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = ForeignKey(to="", on_delete=models.CASCADE)
    user = ForeignKey(to="", on_delete=models.SET_NULL)
