from django import forms

from cards.models import Series, Card


class GenerateForm(forms.Form):
    series = forms.ModelChoiceField(
        queryset=Series.objects.all(),  label='Серия', empty_label=None)
    duration = forms.ChoiceField(
        choices=Card.DURATION, label='Срок окончания активности')

    quantity = forms.IntegerField(label='Количество', min_value=1)