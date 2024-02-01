from typing import Dict

from django.http import HttpRequest

from products.models import Category


def categories_obj(request: HttpRequest) -> Dict:
    "Возвращает данные для отображения в базовом шаблоне категории"

    return {"categories": Category.objects.all()}
