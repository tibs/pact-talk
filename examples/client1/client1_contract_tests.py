#!/usr/bin/env python3

import atexit
import requests

from pact import Consumer, Provider

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
