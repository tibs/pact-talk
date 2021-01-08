#!/usr/bin/env python3

import requests

BASE_URL = 'http://localhost:8080'

def test_buttering():
    result = requests.get(f'{BASE_URL}/butter/bread')
    assert(result.status_code) == 200
    assert(result.text) == 'bread and butter'

def test_buttering_twice():
    result = requests.get(f'{BASE_URL}/butter/bread%20and%20butter')
    assert(result.status_code) == 200
    assert(result.text) == 'bread and butter'

def test_info():
    result = requests.get(f'{BASE_URL}/info')
    json_result = result.json()
    assert json_result['lactose'] in (True, False)
    salt = json_result['salt']
    assert salt[-1] == '%'
    assert float(salt[:-1]) >= 0.0
