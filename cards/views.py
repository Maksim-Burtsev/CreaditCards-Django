from django.shortcuts import redirect, render

from cards.models import Card, Series
from cards.forms import GenerateForm

import random
import pytz
import datetime
from dateutil.relativedelta import relativedelta


def index(request):
    """Обрабатывает главную страницу со списом всех карт"""

    cards = Card.objects.all()

    context = {
        'cards': cards,
    }

    return render(request, 'cards/index.html', context=context)


def generate(request):
    """Генерирует банковские карты"""

    if request.method == 'POST':

        series_id = int(request.POST.get('series'))
        quantity = int(request.POST.get('quantity'))
        duration = int(request.POST.get('duration'))

        generated_cards_number = _generate_card_numbers(quantity, series_id)

        series = Series.objects.get(id=series_id)
        date_created = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
        end_date = date_created + relativedelta(months=duration)

        context = {
            'series': series,
            'numbers': generated_cards_number,
            'date_created': date_created,
            'end_date': end_date,
            'status': 'Не активирована'
        }

        return render(request, 'cards/generate_result.html', context=context)

    form = GenerateForm()
    context = {
        'form': form,
    }

    return render(request, 'cards/generate.html', context=context)


def profile(request, card_number):
    """Страница карты"""
    card = Card.objects.get(number=card_number)
    balance = f'{card.balance:,}'.replace(',', ' ')
    context = {
        'card': card,
        'balance' : balance,
    }

    return render(request, 'cards/profile.html', context=context)

def activate(request, card_number):
    """Активирует карту"""
    card = Card.objects.get(number=card_number)
    card.status = 'active'
    card.save()
    
    return redirect('profile', card.number)

def deactivate(request, card_number):
    """Деактивирует карту"""
    card = Card.objects.get(number=card_number)
    card.status = 'inactivated'
    card.save()
    
    return redirect('profile', card.number)

def delete(reques, card_number):
    """Удаляет карту"""
    card = Card.objects.get(number=card_number)
    card.delete()

    return redirect('home')

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
