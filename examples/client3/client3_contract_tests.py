#!/usr/bin/env python3

import atexit
import requests

from pact import Consumer, Provider, Term, Like

pact = Consumer('sandwich-maker').has_pact_with(Provider('Butterer'))
pact.start_service()
atexit.register(pact.stop_service)

PACT_BASE_URL = 'http://localhost:1234'

BREAD_AND_BUTTER = 'bread and butter'

def test_buttering():

    (pact
     .given('We want to butter bread')
     .upon_receiving('a request to butter bread')
     .with_request('get', '/butter/bread')
     .will_respond_with(200, body=BREAD_AND_BUTTER))

    with pact:
        result = requests.get(f'{PACT_BASE_URL}/butter/bread')

    assert result.text == 'bread and butter'

def test_buttering_twice():

    (pact
     .given('We want to butter bread again')
     .upon_receiving('a request to butter buttered bread')
     .with_request('get', '/butter/bread%20and%20butter')
     .will_respond_with(200, body=BREAD_AND_BUTTER))

    with pact:
        result = requests.get(f'{PACT_BASE_URL}/butter/bread%20and%20butter')

    assert result.text == 'bread and butter'

BUTTER_INFO = Like(
    {
        'salt': Term(r'\d+(\.\d+)?%', '0%'),
        'lactose': False,
    }
)

def test_info():

    (pact
     .given('We want to know about the butter being used')
     .upon_receiving('a request for information')
     .with_request('get', '/info')
     .will_respond_with(200, body=BUTTER_INFO))

    with pact:
        result = requests.get(f'{PACT_BASE_URL}/info')

    json_result = result.json()
    assert json_result['lactose'] in (True, False)
    salt = json_result['salt']
    assert salt[-1] == '%'
    assert float(salt[:-1]) >= 0.0
