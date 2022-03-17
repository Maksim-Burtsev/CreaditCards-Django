from django.shortcuts import redirect, render

from cards.models import Card, Series
from cards.forms import GenerateForm, SearchForm
from cards.services import _generate_card_numbers, _search_results

import pytz
import datetime
from dateutil.relativedelta import relativedelta


def index(request):
    """Обрабатывает главную страницу со списом всех карт"""

    if request.GET.get('search'):
        cards = _search_results(request.GET.get('search'))

    else:
        cards = Card.objects.all()

    form = SearchForm()

    context = {
        'cards': cards,
        'form': form,
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
        'balance': balance,
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



