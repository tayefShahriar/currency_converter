from django.urls import path
from .views import CurrencyList, ConvertCurrency
urlpatterns = [
    path('convert/<str:from_currency>/<str:to_currency>/<str:amount>/', ConvertCurrency.as_view(), name='convert_currency'),
    path('currencies/', CurrencyList.as_view(), name='currencylist'),
]
