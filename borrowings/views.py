import datetime

from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowingReturnSerializer
import telegram

from django.conf import settings
from django.template.loader import render_to_string


class BorrowingsViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")

        queryset = self.queryset
        if user_id:
            queryset = queryset.filter(user_id=int(user_id))

        if is_active == "True":
            queryset = queryset.exclude(actual_return_date__isnull=False)

        if is_active == "False":
            queryset = queryset.exclude(actual_return_date__isnull=True)

        return queryset.distinct()

    def get_serializer_class(self):

        if self.action == "return_":
            return BorrowingReturnSerializer

        return self.serializer_class

    @transaction.atomic
    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
    )
    def return_(self, request, pk=None):
        borrowing = Borrowing.objects.get(pk=pk)

        if not borrowing.actual_return_date:
            borrowing.actual_return_date = datetime.date.today()
            borrowing.save()
            book = borrowing.book
            book.inventory += 1
            book.save()

            return Response(status=status.HTTP_200_OK)

        return Response(f"message:This borrow is closed at {borrowing.actual_return_date}")


def post_borrowing_on_telegram(borrowing):
    message_html = render_to_string('telegram_message.html', {
        'borrowing': borrowing
    })
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token=telegram_settings['bot_token'])
    bot.send_message(chat_id="@%s" % telegram_settings['chat_name'],
                     text=message_html, parse_mode=telegram.ParseMode.HTML)
