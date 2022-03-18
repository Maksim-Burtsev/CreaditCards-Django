from django.test import TestCase
from django.utils import timezone


from cards.services import _generate_card_numbers, _search_results
from cards.models import Series, Card


class ServicesGeneratorTest(TestCase):
    TEST_CARD_QUANTITY = 100
    CORRECT_NUM_LEN = 10

    def test_card_generator(self):
        _series = Series()
        _series.card_series = 222222
        _series.save()

        result = _generate_card_numbers(
            ServicesGeneratorTest.TEST_CARD_QUANTITY, _series.id)

        self.assertEqual(len(result), 100)
        self.assertEqual(len(set(result)), 100)

    def test_cards_len(self):

        all_len_num_correct = True

        _series = Series()
        _series.card_series = 333333
        _series.save()

        result = _generate_card_numbers(
            ServicesGeneratorTest.TEST_CARD_QUANTITY, _series.id)

        for num in result:
            if len(str(num)) != ServicesGeneratorTest.CORRECT_NUM_LEN:
                all_len_num_correct = False
                break

        self.assertTrue(all_len_num_correct)

    def test_cards_is_digit(self):

        all_len_num_digit = True

        _series = Series()
        _series.card_series = 444444
        _series.save()

        result = _generate_card_numbers(
            ServicesGeneratorTest.TEST_CARD_QUANTITY, _series.id)

        for num in result:
            if not isinstance(num, int):
                all_len_num_digit = False
                break

        self.assertTrue(all_len_num_digit)


class ServicesSearchTest(TestCase):

    def test_search(self):

        _series = Series()
        _series.card_series = 123456
        _series.save()

        for i in range(10):
            _card = Card.objects.create(
                series_id=_series.id,
                number=1234566789+i,
                duration=6,
                balance=1000,
                status='active',
            )

        test_card = Card.objects.first()
        end_date = test_card.end_date.date()

        search_1 = _search_results('1234')
        self.assertEqual(len(search_1), 10)
        
        search_2 = _search_results('active')
        self.assertEqual(len(search_2), 10)

        search_3 = _search_results('6')
        self.assertEqual(len(search_3), 10)

        date_now = timezone.now().date()
        search_4 = _search_results(str(date_now))
        self.assertEqual(len(search_4), 10)

        search_5 = _search_results('123456678')
        self.assertEqual(len(search_5), 1)

        search_6 = _search_results('123456679')
        self.assertEqual(len(search_6), 9)

        search_7 = _search_results('wrong')
        self.assertEqual(len(search_7), 0)

        search_8 = _search_results(str(end_date))
        self.assertEqual(len(search_8), 10)