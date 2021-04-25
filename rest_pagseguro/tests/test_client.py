from unittest import mock

from django.conf import settings
from rest_framework.test import APITestCase

from rest_pagseguro.client import PagSeguro


class PagSeguroClientTestCase(APITestCase):
    
    def setUp(self):
        settings.PAGSEGURO = {
            'sandbox': True,
            'client': {
                'email': 'test@django.com',
                'token': 'randomtoken'
            }
        }

    def test_create_pagseguro_session():
        """
        Testa o caso de sucesso da criação de uma sessão
        """
        
        pagseguro = PagSeguro()
        pagseguro._make_request = mock.MagicMock(
            return_value=(
                '<?xml version="1.0" encoding="ISO-8859-1"?>'
                '<session>'
                '<id>620f99e348c24f07877c927b353e49d3</id>'
                '</session>'
            )
        )

        assert pagseguro.create_session() == '620f99e348c24f07877c927b353e49d3'
        