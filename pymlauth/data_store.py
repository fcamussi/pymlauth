#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 14:55:16 2025

@author: Fernando Camussi
"""
import json


class DataStore:

    class ParamKeys:
        CLIENT_ID = 'client_id'
        CLIENT_SECRET = 'client_secret'
        REDIRECT_URI = 'redirect_uri'
        REFRESH_TOKEN = 'refresh_token'

    def __init__(self, filepath):
        self.filepath = filepath
        self.data = self._load_data()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self._save_data()

    def _load_data(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_data(self):
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
