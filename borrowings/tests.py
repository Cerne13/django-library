from django.test import TestCase
from rest_framework import status

from borrowings.models import Borrowing
from books.models import Book
from user.models import Customer


from rest_framework.test import APIClient

BORROWING_URL = "/api/borrowings/"


class UnauthenticatedBorrowingApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(BORROWING_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBorrowingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="test@test.com",
            password="test1234",
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            inventory=1,
            daily_fee=1,
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.customer,
            expected_return_date="2021-01-01",
        )
        self.client.force_authenticate(self.customer)

    def test_list_borrowing(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["book"], self.book.id)
        self.assertEqual(response.data[0]["user"], self.customer.id)
        self.assertEqual(response.data[0]["expected_return_date"], "2021-01-01")

    def test_create_borrowing(self):
        response = self.client.post(
            BORROWING_URL,
            {
                "book": self.book.id,
                "user": self.customer.id,
                "expected_return_date": "2021-01-01",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["book"], self.book.id)
        self.assertEqual(response.data["user"], self.customer.id)
        self.assertEqual(response.data["expected_return_date"], "2021-01-01")

    def test_filter_borrowing_is_active(self):
        response = self.client.get(BORROWING_URL, {"is_active": True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["book"], self.book.id)
        self.assertEqual(response.data[0]["user"], self.customer.id)
        self.assertEqual(response.data[0]["expected_return_date"], "2021-01-01")

    def test_filter_borrowing_user_id(self):
        response = self.client.get(BORROWING_URL, {"user_id": self.customer.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["book"], self.book.id)
        self.assertEqual(response.data[0]["user"], self.customer.id)
        self.assertEqual(response.data[0]["expected_return_date"], "2021-01-01")

    def test_borrowing_return(self):
        response = self.client.put(
            f"{BORROWING_URL}{self.borrowing.id}/return/",
            {"actual_return_date": "2021-01-01"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["book"], self.book.id)
        self.assertEqual(response.data["user"], self.customer.id)
        self.assertEqual(response.data["expected_return_date"], "2021-01-01")
        self.assertEqual(response.data["actual_return_date"], "2021-01-01")

    def test_borrowing_date_validation(self):
        response = self.client.post(
            BORROWING_URL,
            {
                "book": self.book.id,
                "user": self.customer.id,
                "expected_return_date": "2020-01-01",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["expected_return_date"][0], "You must select correct return date")

    def test_borrowing_inventory_validation(self):
        response = self.client.post(
            BORROWING_URL,
            {
                "book": self.book.id,
                "user": self.customer.id,
                "expected_return_date": "2021-01-01",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["book"][0], f"{self.book.title} is end")
