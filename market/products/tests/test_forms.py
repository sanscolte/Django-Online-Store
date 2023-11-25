from django.test import TestCase

from products.forms import ReviewForm
from products.models import Review


class ReviewFormTest(TestCase):
    """Класс тестов для формы Review"""

    def test_valid_form(self):
        data: dict[str, int] = {"text": "test review", "rating": 5}
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_text_form(self):
        """Тестирование формы с текстом превышающем валидное значение"""

        max_length: int = int(Review._meta.get_field("text").max_length) + 1
        text: str = "_" * max_length
        data: dict[str, int] = {"text": text, "rating": 5}
        form = ReviewForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_rating_form(self):
        """Тестирование формы с некорректными значениями рейтинга"""

        incorrect_values: list[int] = [-1, 6]

        for value in incorrect_values:
            data: dict[str, int] = {"text": "test review", "rating": value}
            form = ReviewForm(data=data)
            self.assertFalse(form.is_valid())
