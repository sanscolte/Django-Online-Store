from django.test import TestCase
from django.urls import reverse


class MyLoginViewTest(TestCase):
    """Класс для тестирования страницы для входа пользователя"""

    def test_login_page_exist_at_desired_location(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Войти")
