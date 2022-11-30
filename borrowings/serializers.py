import datetime

from rest_framework import serializers

from borrowings.models import Borrowing

import telegram

from django.conf import settings
from django.template.loader import render_to_string


def post_borrowing_on_telegram(borrowing):
    message_html = render_to_string('telegram_message.html', {
        'borrowing': borrowing
    })
    telegram_settings = settings.TELEGRAM
    bot = telegram.Bot(token=telegram_settings['bot_token'])
    bot.send_message(chat_id="@%s" % telegram_settings['chat_name'],
                     text=message_html, parse_mode=telegram.ParseMode.HTML)


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]
        read_only_fields = [
            "id",
            "borrow_date",
            "actual_return_date",
        ]

    @staticmethod
    def validate_inventory(data):
        book_inventory = data["book"].inventory
        if not book_inventory:
            raise serializers.ValidationError(
                f"No more {data['book'].title} in stock"
            )

    @staticmethod
    def validate_date(data):
        if datetime.date.today() > data["expected_return_date"]:
            raise serializers.ValidationError(
                "You must select a correct return date"
            )

    def validate(self, attrs):
        data = super(BorrowingSerializer, self).validate(attrs=attrs)
        self.validate_inventory(data)
        self.validate_date(data)

        return data

    def create(self, validated_data):
        validated_data["book"].inventory -= 1
        validated_data["book"].save()

        borrowing = Borrowing.objects.create(**validated_data)
        post_borrowing_on_telegram(borrowing)

        return borrowing


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["id", "user"]
