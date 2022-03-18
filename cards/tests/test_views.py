from django.test import TestCase
from django.urls import reverse

from cards.models import Card, Series


class CardsViewsTest(TestCase):

    def test_index(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/index.html')

    def test_generate_POST(self):

        _series = Series.objects.create(
            card_series=234561,
        )

        response = self.client.post(
            reverse('generate'),
            {
                'series': _series.id,
                'quantity': 10,
                'duration': 12,
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/generate_result.html')

    def test_bad_generate_POST(self):

        _series = Series.objects.create(
            card_series=234776,
        )
        wrong_duration = 12341
        bad_response = self.client.post(
            reverse('generate'),
            {
                'series': _series.id,
                'quantity': 10,
                'duration': wrong_duration,
            }

        )
        self.assertTemplateUsed(bad_response, 'cards/generate.html')

    def test_generate_GET(self):

        response = self.client.get(reverse('generate'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/generate.html')

    def test_profile(self):

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

        response = self.client.get(
            reverse('profile', kwargs={'card_number': _card.number}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/profile.html')

    def test_activate(self):
        _series = Series.objects.create(
            card_series=234563,
        )

        _card = Card.objects.create(
            series_id=_series.id,
            number=2414566782,
            duration=6,
            balance=1000,
            status='inactivated',
        )

        response = self.client.get(
            reverse('activate', kwargs={'card_number': _card.number}))

        self.assertEqual(response.status_code, 302)

        _card = Card.objects.get(number=2414566782)
        self.assertEqual(_card.status, 'active')

    def test_deactivate(self):
        _series = Series.objects.create(
            card_series=224563,
        )

        _card = Card.objects.create(
            series_id=_series.id,
            number=2414536782,
            duration=6,
            balance=1000,
            status='active',
        )

        response = self.client.get(
            reverse('deactivate', kwargs={'card_number': _card.number}))

        self.assertEqual(response.status_code, 302)

        _card = Card.objects.get(number=2414536782)
        self.assertEqual(_card.status, 'inactivated')

    def test_delete(self):
        _series = Series.objects.create(
            card_series=224363,
        )

        _card = Card.objects.create(
            series_id=_series.id,
            number=2114536782,
            duration=6,
            balance=1000,
            status='active',
        )

        self.assertEqual(Card.objects.count(), 1)

        response = self.client.get(
            reverse('delete', kwargs={'card_number': _card.number}))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Card.objects.count(), 0)

    def test_search(self):

        response = self.client.get(
            reverse('home'), kwargs={'search': '2022'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/index.html')
