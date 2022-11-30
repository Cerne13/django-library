import datetime

from django.core.exceptions import ValidationError
from rest_framework import serializers

from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user"

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

        return Borrowing.objects.create(**validated_data)


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "user"

        ]
