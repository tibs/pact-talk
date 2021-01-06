#!/usr/bin/env python3

from server2 import butter

def test_butter():
    assert butter('bread') == 'bread and butter'

def test_already_buttered():
    assert butter('bread and butter') == 'bread and butter'
