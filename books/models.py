from django.db import models


class Book(models.Model):
    COVER_CHOICES = [("hard", "HARD"), ("soft", "SOFT")]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(
        max_length=4,
        choices=COVER_CHOICES,
        default="hard"
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title
