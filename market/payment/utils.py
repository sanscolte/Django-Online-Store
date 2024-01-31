import re

card_number_pattern: str = r"^\d{7}[2468]$"


def card_number_is_valid(card_number: str) -> bool:
    """
    Проверяет, является ли номер карты 8-значным четным числом, не заканчивающимся на 0
    :param card_number: Номер карты
    :return: Валидность карты
    """
    card_number: str = "".join(card_number.split())
    return True if re.fullmatch(card_number_pattern, card_number) else False
