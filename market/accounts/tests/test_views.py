from django.test import TestCase
from django.urls import reverse


class MyRegistrationViewTest(TestCase):
    """Класс для тестирования страницы регистрации пользователя"""

    fixtures = ["fixtures/01-users.json"]

    def test_registration_page_exist_at_desired_location(self):
        response = self.client.get(reverse("accounts:registration"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Зарегистрироваться")

    def test_registration_page_redirect_if_loged(self):
        self.client.login(email="demon_at@mail.ru", password="61903991shalaikodima")
        response = self.client.get(reverse("accounts:registration"))
        self.assertRedirects(
            response=response, expected_url=reverse("accounts:my-account"), status_code=302, target_status_code=200
        )

    def test_registration_page_post(self):
        response = self.client.post(
            reverse("accounts:registration"),
            {
                "password1": "Wqdsfsgsg1421!",
                "password2": "Wqdsfsgsg1421!",
                "full_name": "test_user",
                "email": "test2@test.ru",
                "phone_number": "1234567890",
            },
        )
        self.assertRedirects(
            response=response, expected_url=reverse("accounts:my-account"), status_code=302, target_status_code=200
        )


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
