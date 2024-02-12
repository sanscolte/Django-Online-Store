from django.test import TestCase
from django.urls import reverse


class MyRegistrationViewTest(TestCase):
    """Класс для тестирования страницы регистрации пользователя"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
    ]

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


class ProfileViewTest(TestCase):
    """Класс для тестирования страницы изменения пользователя"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
    ]

    def test_profile_page_exist_at_desired_location(self):
        self.client.login(email="demon_at@mail.ru", password="61903991shalaikodima")
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Сохранить")

    def test_profile_page_redirect_if_user_no_login(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertRedirects(
            response=response, expected_url="/ru/login/?next=/ru/profile/", status_code=302, target_status_code=200
        )

    def test_profile_page_successfully(self):
        self.client.login(email="demon_at@mail.ru", password="61903991shalaikodima")
        response = self.client.post(
            reverse("accounts:profile"),
            {
                "password1": "Wqdsfsgsg1421!",
                "password2": "Wqdsfsgsg1421!",
                "full_name": "test_user",
                "email": "test2@test.ru",
                "phone_number": "1234567890",
                "avatar": "(binary)",
            },
        )
        self.assertRedirects(
            response=response, expected_url=reverse("accounts:profile"), status_code=302, target_status_code=302
        )


class PasswordResetViewViewTest(TestCase):
    """Класс для тестирования страницы изменения пароля пользователя"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
    ]

    def test_reset_password_page_exist_at_desired_location(self):
        response = self.client.get(reverse("accounts:password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "введите адрес электронной почты")

    def test_password_reset_done_page_successfully(self):
        response = self.client.post(reverse("accounts:password_reset"), {"email": "demon_at@mail.ru"})
        self.assertRedirects(
            response=response,
            expected_url=reverse("accounts:password_reset_done"),
            status_code=302,
            target_status_code=200,
        )


class MyLoginViewTest(TestCase):
    """Класс для тестирования страницы для входа пользователя"""

    def test_login_page_exist_at_desired_location(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Войти")


class AccountViewTest(TestCase):
    """Класс для тестирования личного кабинета пользователя"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
    ]

    def test_account_page_exist_at_desired_location(self):
        self.client.login(email="demon_at@mail.ru", password="61903991shalaikodima")
        response = self.client.get(reverse("accounts:my-account"))
        self.assertEqual(response.status_code, 200)

    def test_account_page_access_without_login(self):
        response = self.client.get(reverse("accounts:my-account"))
        self.assertEqual(response.status_code, 302)
