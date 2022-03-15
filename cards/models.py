from django.db import models
from django.core.exceptions import ValidationError

import datetime
from dateutil.relativedelta import relativedelta


class Series(models.Model):
    """Серия карты"""

    card_series = models.PositiveIntegerField('Серия карты')

    def clean(self, *args, **kwargs) -> None:
        if len(str(self.card_series)) == 6:
            return super().clean(*args, **kwargs)
        raise ValidationError('Код банка - шестизначное число!')

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.card_series)

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'


class Card(models.Model):
    """Банковская карта"""

    CARD_STATUS = [
        ('active', 'Активирована'),
        ('inactivated', 'Не активирована'),
        ('overdue', 'Просрочена')
    ]

    DURATION = [
        (1, '1 месяц'),
        (6, '6 месяцев'),
        (12, '1 год'),
    ]

    series = models.ForeignKey(Series, on_delete=models.CASCADE,
                               related_name='cards', verbose_name='Серия')

    number = models.PositiveIntegerField('Номер карты', unique=True)

    release_time = models.DateTimeField('Дата выпуска', blank=True, null=True)

    duration = models.PositiveIntegerField(
        'Длительность действия', choices=DURATION)

    end_date = models.DateTimeField(
        'Дата окончания активности', blank=True, null=True)

    last_use = models.DateTimeField('Последнее использование', auto_now=True)

    balance = models.DecimalField('Баланс', max_digits=10, decimal_places=2)

    status = models.CharField('Статус карты', max_length=255,
                              choices=CARD_STATUS)

    def clean(self, *args, **kwargs):
        if len(str(self.number)) == 10:
            return super().clean(*args, **kwargs)
        raise ValidationError('Номер карты состоит из 10 цифр!')

    def save(self, *args, **kwargs) -> None:
        self.full_clean()

        if not self.release_time and not self.end_date:
            self.release_time = datetime.datetime.now()
            self.end_date = self.release_time + \
                relativedelta(months=self.duration)
    #TODO решить проблему со временм
        if datetime.datetime.now() >= self.end_date:
            self.status = 'overdue'

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'


class Shopping(models.Model):
    """Покупки"""

    name = models.CharField('Название покупки', max_length=255)

    card = models.ForeignKey(Card, on_delete=models.CASCADE,
                             related_name='shopping', verbose_name='Банковская карта')

    cost = models.DecimalField('Стоимость покупки', max_digits=10,
                               decimal_places=2)

    residual = models.DecimalField('Остаток на карте', max_digits=10,
                                   decimal_places=2, blank=True, null=True)

    buy_time = models.DateTimeField('Время покупки', auto_now_add=True)

    def clean(self, *args, **kwargs):
        if self.cost <= self.card.balance:
            return super().clean(*args, **kwargs)
        raise ValidationError('На счёте недостаточно средств')

    def save(self, *args, **kwargs):
        self.full_clean()

        self.residual = self.card.balance - self.cost
        super().save(*args, *kwargs)

    def __str__(self) -> str:
        return f'{self.name} {self.card}'

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
