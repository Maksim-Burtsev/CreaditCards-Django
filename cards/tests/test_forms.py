from django.test import TestCase

from cards.forms import GenerateForm, SearchForm
from cards.models import Series, Card


class CardsFormsTest(TestCase):

    def test_generate_form(self):
        _series = Series()
        _series.card_series = 111111
        _series.save()

        form = GenerateForm(data={
            'series': _series.id,
            'duration': 12,
            'quantity': 10,
        })

        self.assertTrue(form.is_valid())

    def test_wrong_generate_form(self):

        wrong_duration = 1234

        _series = Series()
        _series.card_series = 222222
        _series.save()

        form = GenerateForm(data={
            'series': _series.id,
            'duration': wrong_duration,
            'quantity': 10,
        })

        self.assertFalse(form.is_valid())

    def test_search_form(self):

        form = SearchForm(data={
            'search': 'test_search',
        })

        self.assertTrue(form.is_valid())
