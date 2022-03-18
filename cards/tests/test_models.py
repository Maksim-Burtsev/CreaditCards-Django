from django.forms import ValidationError
from django.test import TestCase

from cards.models import Series, Card, Shopping


class SeriesModelTest(TestCase):

    def test_series(self):
        _series = Series.objects.create(
            card_series=123456,
        )

        self.assertEqual(_series.card_series, 123456)

        self.assertEqual(str(_series), '123456')

    def test_wrong_series(self):

        _series = Series()
        _series.card_series = 123421251

        self.assertRaises(ValidationError, _series.clean)

class CardModelTest(TestCase):

    def test_card(self):

        _series = Series()
        _series.card_series=123456
        _series.save()

        _card = Card.objects.create(
            series_id=_series.id,
            number=1234566789,
            duration=1,
            balance=1000,
            status='active',
        )

        self.assertEqual(_card.series_id, _series.id)
        self.assertEqual(_card.number, 1234566789)
        self.assertEqual(_card.duration, 1)
        self.assertEqual(_card.balance, 1000)
        self.assertEqual(_card.status, 'active')
        self.assertEqual(str(_card), '123456 1234566789')

    def test_wrong_card(self):
        _series = Series.objects.create(
            card_series=123456,
        )

        _card = Card()
        _card.series_id=1,
        _card.number=1294122111111,
        _card.duration=1,
        _card.balance=1000,
        _card.status='active'

        self.assertRaises(ValidationError, _card.clean)

class ShoppingModelTest(TestCase):

    def test_shopping(self):
        
        _series = Series.objects.create(
            card_series=234561,
        )

        _card = Card.objects.create(
            series_id=_series.id,
            number=2414566789,
            duration=6,
            balance=1000,
            status='active',
        )
        _shopping = Shopping()

        _shopping.name = 'Тестовая покупка'
        _shopping.card_id = _card.id
        _shopping.cost = 100
        _shopping.save()

        self.assertEqual(_shopping.name, 'Тестовая покупка')
        self.assertEqual(_shopping.card.id, _card.id)
        self.assertEqual(_shopping.cost, 100)
        self.assertEqual(_shopping.residual, 900)

    def test_wrong_cost(self):
        _series = Series.objects.create(
            card_series=234561,
        )

        _card = Card.objects.create(
            series_id=_series.id,
            number=2414566789,
            duration=6,
            balance=1000,
            status='active',
        )
        _shopping = Shopping()

        _shopping.name = 'Тестовая покупка'
        _shopping.card_id = _card.id
        _shopping.cost = 7777777
        
        self.assertRaises(ValidationError, _shopping.clean)

    def test_wrong_with_card(self):
        _series = Series.objects.create(
            card_series=234561,
        )

        _card = Card.objects.create(
            series_id=_series.id,
            number=2414566789,
            duration=6,
            balance=1000,
            status='inactivated',
        )

        _card2 = Card.objects.create(
            series_id=_series.id,
            number=1234098760,
            duration=1,
            balance=1000,
            status='overdue',
        )

        _shopping = Shopping()

        _shopping.name = 'Тестовая покупка'
        _shopping.card_id = _card.id
        _shopping.cost = 100

        _shopping2 = Shopping()

        _shopping2.name = 'Тестовая покупка'
        _shopping2.card_id = _card2.id
        _shopping2.cost = 100
        
        self.assertRaises(ValidationError, _shopping.clean)
        self.assertRaises(ValidationError, _shopping2.clean)