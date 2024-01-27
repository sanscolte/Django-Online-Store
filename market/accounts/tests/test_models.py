from django.test import TestCase
from accounts.models import User


class UserFixturesTest(TestCase):
    """Класс тестов фикстур модели Пользователя"""

    fixtures = [
        "fixtures/01-users.json",
        "fixtures/01-users-permissions.json",
        "fixtures/01-groups.json",
    ]

    def test_fixtures_len(self):
        self.assertEqual(User.objects.count(), 8)


class UserModelTest(TestCase):
    """Класс тестов для модели пользователя"""

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(email="test@test.ru")
        user.set_password("123456")
        user.save()

    def test_verbose_name(self):
        user = User.objects.get(email="test@test.ru")
        field_verboses = {
            "email": "Email адрес",
            "full_name": "Полное имя",
            "avatar": "Аватар",
            "phone_number": "Телефон",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(user._meta.get_field(field).verbose_name, expected_value)

    def test_max_phone_number(self):
        user = User.objects.get(email="test@test.ru")
        max_length = user._meta.get_field("phone_number").max_length
        self.assertEqual(max_length, 12)

    def test_email_unique(self):
        user = User.objects.get(email="test@test.ru")
        unique = user._meta.get_field("email").unique
        self.assertTrue(unique)

    def test_phone_number_unique(self):
        user = User.objects.get(email="test@test.ru")
        unique = user._meta.get_field("phone_number").unique
        self.assertTrue(unique)
