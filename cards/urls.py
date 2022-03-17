from django.urls import path

from cards.views import index, generate, profile, activate, deactivate, delete  


urlpatterns = [
    path('', index, name='home'),
    path('generate', generate, name='generate'),
    path('profile/<int:card_number>', profile, name='profile'),
    path('activate/<int:card_number>', activate, name='activate'),
    path('deactivate/<int:card_number>', deactivate, name='deactivate'),
    path('delete/<int:card_number>', delete, name='delete'),
]
