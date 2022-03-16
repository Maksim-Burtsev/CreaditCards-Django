from django.urls import path

from cards.views import index, generate, profile    


urlpatterns = [
    path('', index, name='home'),
    path('generate', generate, name='generate'),
    path('profile/<int:card_number>', profile, name='profile')
]
