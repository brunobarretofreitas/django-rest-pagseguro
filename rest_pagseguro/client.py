from urllib.parse import urljoin

import requests
from django.conf import settings
from rest_framework import exceptions

from .exceptions import PagSeguroSettingsException
from .constants import api as api_constants
from .parsers import parse_session_id


class PagSeguro:
    """API Client da Pague Seguro"""

    # Excessões retornadas da PagSeguro
    EXCEPTION_MAP = {
        400: exceptions.ValidationError,
        401: exceptions.AuthenticationFailed,
        403: exceptions.PermissionDenied,
        405: exceptions.MethodNotAllowed,
        415: exceptions.UnsupportedMediaType,
        500: exceptions.APIException
    }   
    
    def __init__(self):
        try:
            self.CLIENT_EMAIL = settings.PAGSEGURO['client']['email']
            self.CLIENT_TOKEN = settings.PAGSEGURO['client']['token']
            # Is Sandbox Environment
            sandbox = settings.PAGSEGURO.get('sandbox', True)
            # Set URL based on Environment
            self.API_URL = (
                api_constants.PAGSEGURO_SANDBOX_URL if sandbox
                else api_constants.PAGSEGURO_URL
            )
        except TypeError:
            raise PagSeguroSettingsException(
                'Configurações de cliente da PagSeguro incorretas.'
            )
    
    def _make_request(self, url, method, **kwargs):
        """
        Método responsável por montar uma requisição à PagSeguro

        Parameters:
            url (str): URL do serviço da Pagseguro (ex: 'sessions')
            
            method (str): Method HTTP (POST, GET, PUT)

            kwargs (dict): Qualquer outro parâmetro para a lib requests 
            (ex: params)

        Returns:
            response (requests.Response): Response da chamada de requests

        """
        request_kwargs = {
            'url': urljoin(self.API_URL, url),
            'method': method,
            'params': {
                'email': self.CLIENT_EMAIL,
                'token': self.CLIENT_TOKEN,
            },
            'headers': {
                'Accept': (
                    'application/vnd.pagseguro.com.br.v3+json;'
                    'charset=ISO-8859-1'
                ),
                'Content-Type': 'application/json',
            },
            **kwargs,
        }

        response = requests.request(**request_kwargs)

        if not response.ok:
            raise self.EXCEPTION_MAP.get(
                response.status_code,
                exceptions.APIException,
            )(detail=response.json(), code=response.status_code)

        return response 

    def create_session(self) -> str:
        """
        Serviço responsável por criar uma sessão com a Pague Seguro

        Returns:
            session (str): Código da sessão criada
        """
        response = self._make_request(url='sessions', method='POST', headers={})

        return parse_session_id(response.text)
