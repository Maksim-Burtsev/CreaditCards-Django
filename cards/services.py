import random
from datetime import timedelta

from cards.models import Card

def _generate_card_numbers(n, series_id) -> list:
    """Генерирует указанное количество уникальных номеров банковской карты"""

    MIN_NUMBER = 1000000000
    MAX_NUMBER = 9999999999
    generated_list = []
    created = 0

    cards = Card.objects.filter(series_id=int(series_id))
    cards_nums = [card.number for card in cards]

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
        msk_release_time = card.release_time + timedelta(hours=3) 
        msk_end_time = card.end_date + timedelta(hours=3)

        if search in str(card.series) and cards not in res:
            res.append(card)

        elif search in str(card.number) and cards not in res:
            res.append(card)

        elif search in str(msk_release_time) and cards not in res:
            res.append(card)

        elif search in str(msk_end_time) and cards not in res:
            res.append(card)
        
        elif search in str(card.status) and cards not in res:
            res.append(card)
        
    return res
