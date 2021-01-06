#!/usr/bin/env python3

import requests

SERVER_BASE_URL = 'http://localhost:8080/butter'

def test_buttering():
    result = requests.get(f'{SERVER_BASE_URL}/bread')
    assert(result.status_code) == 200
    assert(result.text) == 'bread and butter'
