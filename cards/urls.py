from django.urls import path

from cards.views import index, generate


urlpatterns = [
    path('', index, name='home'),
    path('generate', generate, name='generate'),
]
