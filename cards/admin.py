from django.contrib import admin
from django.utils.safestring import mark_safe

from cards.models import Card, Series, Shopping

admin.site.register(Series)


@admin.register(Shopping)
class ShoppingAdmin(admin.ModelAdmin):
    fields = ('name', 'card', 'cost')
    list_display = ('name', 'card', 'cost', 'buy_time','get_residual')

    def get_residual(self, obj):
        """Форматирует остаток на средст на карте"""
        res = f'{obj.residual:,}'.replace(',', ' ').replace('.', ',')
        if res.split(',')[-1] == '00':
            return f'{res[:-3]}$'
        return f'{res}$'
    
    get_residual.short_description = 'Остаток'

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    fields = ('series', 'number', 'duration', 'balance', 'status')
    list_display = ('series', 'number', 'release_time', 'end_date',
                    'last_use', 'duration', 'balance', 'status')
