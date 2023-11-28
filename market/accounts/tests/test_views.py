from django.test import TestCase
from django.urls import reverse


class MyLoginViewTest(TestCase):
    """Класс для тестирования страницы для входа пользователя"""

    def test_login_page_exist_at_desired_location(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Войти")


class AccountViewTest(TestCase):
    """Класс для тестирования личного кабинета пользователя"""

    fixtures = ["fixtures/01-users.json"]

    def test_account_page_exist_at_desired_location(self):
        self.client.login(email="demon_at@mail.ru", password="61903991shalaikodima")
        response = self.client.get(reverse("accounts:my-account"))
        self.assertEqual(response.status_code, 200)

    def test_account_page_access_without_login(self):
        response = self.client.get(reverse("accounts:my-account"))
        self.assertEqual(response.status_code, 302)
