#!/usr/bin/env python3

import requests

BASE_URL = 'http://localhost:8080'

def test_buttering():
    result = requests.get(f'{BASE_URL}/butter/bread')
    assert(result.status_code) == 200
    assert(result.text) == 'bread and butter'
