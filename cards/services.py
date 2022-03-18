import random

from cards.models import Card


def _generate_card_numbers(n, series_id) -> list:
    """Генерирует указанное количество уникальных номеров банковской карты"""

    MIN_NUMBER = 1000000000
    MAX_NUMBER = 9999999999
    MAX_UNIQUE = 9*(10**9)

    generated_list = []
    created = 0

    cards = Card.objects.filter(series_id=int(series_id))
    cards_nums = [card.number for card in cards]
    len_cards_nums = len(cards_nums)

    if n > MAX_UNIQUE - len(cards_nums):
        n = MAX_UNIQUE - len(cards_nums)

    while created < int(n):

        number = random.randint(MIN_NUMBER, MAX_NUMBER)
        if number not in cards_nums:
            generated_list.append(number)
            created += 1

    return generated_list


def _search_results(search: str) -> list:
    """Выполняет поиск по указанному запросу"""
    res = []
    cards = Card.objects.all()

    for card in cards:

        if search in str(card.series) and cards not in res:
            res.append(card)

        elif search in str(card.number) and cards not in res:
            res.append(card)

        elif search in str(card.release_time) and cards not in res:
            res.append(card)

        elif search in str(card.end_date) and cards not in res:
            res.append(card)

        elif search in str(card.status) and cards not in res:
            res.append(card)

    return res
