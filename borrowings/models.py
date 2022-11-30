from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import ForeignKey

from books.models import Book


# TODO: Add foreign keys to books, users
# TODO: constraints for borrow_date, expected_return_date, and actual_return_date.


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = ForeignKey(Book, on_delete=models.CASCADE)
    user = ForeignKey(get_user_model(), on_delete=models.CASCADE)
