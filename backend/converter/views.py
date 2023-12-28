import requests
import logging
from datetime import timedelta
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Currency, UpdateLog
from .serializers import CurrencySerializer

logger = logging.getLogger(__name__)
EXCHANGE_RATE_API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'
UPDATE_INTERVAL = 1 # hours

class ConvertCurrency(APIView):
    def get(self, request, from_currency, to_currency, amount):
        try:
            self.update_rates_if_necessary()
            return self.perform_conversion(from_currency, to_currency, amount)
        except Exception as e:
            logger.error(str(e))
            return Response({'error': 'Unexpected error'}, status=status.HTTP_500_INTERNAL_SEVER_ERROR)
        
    def update_rates_if_necessary(self):
        try:
            last_updated = UpdateLog.objects.latest('updated_at')
        except UpdateLog.DoesNotExist:
            last_updated = None

        if not last_updated or last_updated.updated_at < timezone.now() - timedelta(hours=UPDATE_INTERVAL):
            self.update_rates()

    def update_rates(self):
        response = requests.get(EXCHANGE_RATE_API_URL)
        data = response.json()

        if 'rates' not in data:
            raise Exception('Could not fetch rates')
        
        for code, rate in data['rates'].items():
            Currency.objects.update_or_create(code=code, defaults={'rate': rate})
        
        UpdateLog.objects.update_or_create(id=1, defaults={'updated_at': timezone.now()})

    def perform_conversion(self, from_currency, to_currency, amount):
        try:
            from_rate = Currency.objects.get(code=from_currency.upper()).rate
            to_rate = Currency.objects.get(code=to_currency.upper()).rate
        except Currency.DoesNotExist:
            return Response({'error': 'Invalid Currency'}, status=status.HTTP_400_BAD_REQUEST)
        
        converted_amount = (float(amount) / from_rate) * to_rate
        return Response({'converted_amount': converted_amount})



class CurrencyList(generics.ListAPIView):
    """ For getting all currencies"""
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
