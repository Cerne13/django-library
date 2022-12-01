from datetime import date, timedelta
import telegram

from django.conf import settings
from django.template.loader import render_to_string

from borrowings.models import Borrowing
from borrowings.serializers import post_borrowing_on_telegram

from dotenv import load_dotenv

load_dotenv()


def notify_of_expired_borrowings():
    tomorrow = date.today() + timedelta(days=1)
    expired_borrowings = Borrowing.objects.filter(
        expected_return_date__lte=tomorrow,
    )
    if expired_borrowings:
        for borrowing in expired_borrowings:
            post_borrowing_on_telegram(borrowing, message_template="telegram_expired_borrowing.html")
    else:
        post_borrowing_on_telegram(message_template="telegram_no_expired_borrowing.html")
