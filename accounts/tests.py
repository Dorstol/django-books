from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class CustomerTests(TestCase):
    def test_user_create(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="Oleh", email="oleh@mail.com", password='testpass123'
        )
        self.assertEqual(user.username, "Oleh")
        self.assertEqual(user.email, "oleh@mail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin = User.objects.create_superuser(
            username="admin", email="superadmin@admin.com", password="test1234"
        )
        self.assertEqual(admin.username, "admin")
        self.assertEqual(admin.email, "superadmin@admin.com")
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)


class SignupPageTests(TestCase):
    username = "newuser"
    email = "newuser@email.com"

    def setUp(self):
        url = reverse("account_signup")
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Sign Up")
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(self.username, self.email)
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
