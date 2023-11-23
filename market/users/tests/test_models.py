from django.test import TestCase
from users.models import User


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
            "phoneNumber": "Телефон",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(user._meta.get_field(field).verbose_name, expected_value)

    def test_max_phoneNumber(self):
        user = User.objects.get(email="test@test.ru")
        max_length = user._meta.get_field("phoneNumber").max_length
        self.assertEqual(max_length, 12)

    def test_email_unique(self):
        user = User.objects.get(email="test@test.ru")
        unique = user._meta.get_field("email").unique
        self.assertTrue(unique)

    def test_phoneNumber_unique(self):
        user = User.objects.get(email="test@test.ru")
        unique = user._meta.get_field("phoneNumber").unique
        self.assertTrue(unique)
