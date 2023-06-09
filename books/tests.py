from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from books.models import Book, Review


class BookTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="reviewuser",
            email="reviewuser@mail.com",
            password="passtest111"
        )

        cls.special_permission = Permission.objects.get(
            codename="special_status"
        )

        cls.book = Book.objects.create(
            title="Witcher",
            author="Andjey Sapkovski",
            price="50.00"
        )

        cls.review = Review.objects.create(
            book=cls.book,
            author=cls.user,
            review="Wonderful book"
        )

    def test_list_book(self):
        self.assertEqual(f"{self.book.title}", "Witcher")
        self.assertEqual(f"{self.book.author}", "Andjey Sapkovski")
        self.assertEqual(f"{self.book.price}", "50.00")

    def test_book_listview_for_logged_in_user(self):
        self.client.login(email="reviewuser@mail.com", password="passtest111")
        responce = self.client.get(reverse("book_list"))
        self.assertEqual(responce.status_code, 200)
        self.assertContains(responce, "Witcher")
        self.assertTemplateUsed(responce, "books/book_list.html")

    def test_book_list_view_for_unlogged_user(self):
        self.client.logout()
        responce = self.client.get(reverse("book_list"))
        self.assertEqual(responce.status_code, 302)

    def test_book_detail_view_with_permission(self):
        self.client.login(email="reviewuser@mail.com", password="passtest111")
        self.user.user_permissions.add(self.special_permission)
        responce = self.client.get(self.book.get_absolute_url())
        no_responce = self.client.get("/books/1488")
        self.assertEqual(responce.status_code, 200)
        self.assertEqual(no_responce.status_code, 404)
        self.assertContains(responce, "Witcher")
        self.assertContains(responce, "Wonderful book")
        self.assertTemplateUsed(responce, "books/book_detail.html")
