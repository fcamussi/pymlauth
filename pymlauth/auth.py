#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 14:54:25 2025

@author: Fernando Camussi
"""
from urllib.parse import urlencode
import requests


class Auth:
    def __init__(self, client_id, client_secret, redirect_uri, refresh_token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.refresh_token = refresh_token
        self.access_token = None

    def authorization_url(self):
        """
        Retorna la URL de autorización.
        """
        base_url = "https://auth.mercadolibre.com.ar/authorization?"
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri
        }
        return base_url + urlencode(params)

    def fetch_tokens(self, auth_code):
        """
        Usa el código de autorización para obtener el token de acceso y el token de refresh.
        """
        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'redirect_uri': self.redirect_uri
        }
        url = "https://api.mercadolibre.com/oauth/token"
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        response_data = response.json()
        self.access_token = response_data['access_token']
        self.refresh_token = response_data['refresh_token']

    def refresh_access_token(self):
        """
        Usa el refresh token para obtener un nuevo token de acceso.
        """
        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
        }
        url = "https://api.mercadolibre.com/oauth/token"
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        response_data = response.json()
        self.access_token = response_data['access_token']
        self.refresh_token = response_data['refresh_token']

    def is_token_valid(self):
        """
        Verifica si el token de acceso ha expirado.
        """
        if not self.access_token:
            return False

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        url = "https://api.mercadolibre.com/users/me"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True
        elif response.status_code == 401:
            # Token inválido o expirado
            return False
        else:
            response.raise_for_status()
            return False

    def get_access_token(self):
        return self.access_token

    def get_refresh_token(self):
        return self.refresh_token
