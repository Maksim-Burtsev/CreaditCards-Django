from dataclasses import field
from django.contrib import admin

from cards.models import Card, Series 

admin.site.register(Series)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    fields = ('series', 'number', 'duration', 'balance', 'status')
    list_display = ('series', 'number', 'release_time', 'end_date', 'last_use','duration', 'balance', 'status')