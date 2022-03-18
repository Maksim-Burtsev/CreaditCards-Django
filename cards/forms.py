from django import forms

from cards.models import Series, Card


class GenerateForm(forms.Form):
    """Форма генерации карт"""

    series = forms.ModelChoiceField(
        queryset=Series.objects.all(),  label='Серия', empty_label=None)
    duration = forms.ChoiceField(
        choices=Card.DURATION, label='Срок окончания активности')
    quantity = forms.IntegerField(label='Количество', min_value=1)

class SearchForm(forms.Form):
    """Форма поиска"""

    search = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Search'}))
