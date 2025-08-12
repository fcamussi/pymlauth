#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 14:55:00 2025

@author: Fernando Camussi
"""
import webbrowser

from pymlauth.auth import Auth
from pymlauth.data_store import DataStore


def main():
    ds = DataStore("auth.json")

    if ds.get(DataStore.ParamKeys.CLIENT_ID) is None:
        ds.set(DataStore.ParamKeys.CLIENT_ID, input("Ingrese Client Id: "))
        ds.set(DataStore.ParamKeys.CLIENT_SECRET, input("Ingrese Client Secret: "))
        ds.set(DataStore.ParamKeys.REDIRECT_URI, input("Ingrese Redirect URI: "))

    auth = Auth(ds.get(DataStore.ParamKeys.CLIENT_ID),
                ds.get(DataStore.ParamKeys.CLIENT_SECRET),
                ds.get(DataStore.ParamKeys.REDIRECT_URI),
                ds.get(DataStore.ParamKeys.REFRESH_TOKEN))

    refresh_token = auth.get_refresh_token()
    if not refresh_token:
        auth_url = auth.authorization_url()
        print(f"Abra esta URL en su navegador si no se abre automáticamente:\n{auth_url}")
        webbrowser.open(auth_url)
        auth_code = input("Ingrese el Auth Code: ")
        auth.fetch_tokens(auth_code)
    else:
        auth.refresh_access_token()
    ds.set(DataStore.ParamKeys.REFRESH_TOKEN, auth.get_refresh_token())

    print(f'Access Token: ' + auth.get_access_token())
    print(f'Token Valido?: {auth.is_token_valid()}')


if __name__ == "__main__":
    main()
