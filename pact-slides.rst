Contract Testing with Pact
==========================

.. class:: titleslideinfo

    By Tibs / Tony Ibbs

    Presented at CamPUG_, virtually, 12th January 2021

    Written in reStructuredText_.

    Converted to PDF slides using rst2pdf_.


Slides to go here
-----------------

No, there is not going to be Fortran in this presentation. This is a
placeholder slide.

.. code:: fortran

  SUBROUTINE CALC(A,B,C,SUM,SUMSQ)
    SUM = A + B + C
    SUMSQ = SUM ** 2
  END

The problem space
-----------------

We have a client application that makes requests to a server.

We want to test this.

Simplest approach
-----------------

The tests talk to a real instance of the server.

Problems:

* We need a server running
* Ideally not the production server
* What version of the server?

Likely to be expensive and slow

Next approach: mock/fake it
---------------------------

We could just write tests that have fixed responses mocked into them.

Problems:

* This is a pain to do for any scale of requests
* What if we get it wrong - our tests may well still pass!
* What version of the server?

Likely to be difficult and unreliable

Better approach - record it
---------------------------

Use a library like VCR or Betamax to record the actual responses

1. Write the tests
2. Run the tests against the real server, recording the responses
3. From then on, use those recorded reponses

Problems:

* What version of the server?

Excellent approach, but it's up to use to remember that we might have
different versions of the server API.

Ideal approach - contract testing
---------------------------------

If we're lucky enough to have at least some control over both client and
server, we can do better.

For instance, if we have

* micro services
* we supply the client and server
* we supply a library that wraps the client and we supply the server
* we have two services talking to each other

Contract testing, summarised
----------------------------

Take the same approach as for VCR/Betamax, but *also* check that the server
believes it will agrees with the recorded request/response pairings.

In other words, we have a **contract** between client and server.

But what about that server version problem?

Add in a contract broker
------------------------

In simple systems, it may be enough for the server and client just to agree
where the contracts are stored, and retrieve them.

But for the complete experience, when generating a contract, also store it,
with an identifying hash, in a contract broker service.

  (conveniently, Pact provides one if you're happy to use it)

Client and server can then be explicit about exactly which contract versions
they both support.

Interlude
---------

<music before the next bit>

A very very simple example
--------------------------

Imagine we are producing a service to make virtual sandwiches.

Since we like microservices (a lot) our main sandwhich assembly service will
need a "put butter on things" service.

The "put butter on things" service, service1
--------------------------------------------

``service1.py``

.. code:: python

  #!/usr/bin/env python3

  from bottle import Bottle

  app = Bottle()

  @app.route('/butter/<substrate>')
  def butter(substrate):
      return f'{substrate} and butter'

  if __name__ == '__main__':
      app.run()

Let's assume that's well tested
-------------------------------

Because of course it is. And there's all the deployment infrastructure we
need, and documentation, and everything, as well.

...OK, here's a basic test
--------------------------

``service1_tests.py``

.. code:: python

  #!/usr/bin/env python3

  from server1 import butter

  def test_butter():
      assert butter('bread') == 'bread and butter'

The test passes
---------------

.. code:: shell

  $ pytest server1_tests.py
  ============================= test session starts ==============================
  platform darwin -- Python 3.8.6, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
  rootdir: /Users/tibs/Dropbox/talks/pact-talk/examples/server1
  collected 1 item

  server1_tests.py .                                                       [100%]

  ============================== 1 passed in 0.05s ===============================

Our client, client1
-------------------

The client for the "put butter on things" service makes an appropriate
request, to get butter put on something, and then carries on with the
rest of the sandwich assembly.

We're not particularly interested in that for now.

We're just interested in the test we need in our client.

(indeed, I didn't actually bother to *write* the actual client...)

The test we need in our client
------------------------------

``client1_tests.py``

.. code:: python


  #!/usr/bin/env python3

  import requests

  BASE_URL = 'http://localhost:8080'

  def test_buttering():
      result = requests.get(f'{SERVER_BASE_URL}/butter/bread')
      assert(result.status_code) == 200
      assert(result.text) == 'bread and butter'

That's it
---------

Since this is the only request from our service to our client, we only have
that one request to test.

Since we know we only ever call it that way, it's not the responsibility of
the server to test what happens if we make any other call - we assume the
client is well tested.

If we test this specific response, then we know that we can assume the result
elsewhere in our testing, and we can use other techniques to inject that
result into that testing - we don't necessarily need to make a request
elsewhere at all.

The test passes
---------------

.. code:: shell

  $ pytest client1_tests.py
  ============================= test session starts ==============================
  platform darwin -- Python 3.8.6, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
  rootdir: /Users/tibs/Dropbox/talks/pact-talk/examples/client1
  collected 1 item

  client1_tests.py .                                                       [100%]

  ============================== 1 passed in 0.10s ===============================

(provided I remember to run the server process)

But - we're making a real request
---------------------------------

Which we already said was a Bad Thing at the start of this talk.

Pact (and VCR and Betamax) all allow us to grab a recording of the request and
response though.

Let's write a test with pact
----------------------------

.. code:: python

  #!/usr/bin/env python3

  import atexit
  import requests

  from pact import Consumer, Provider

  pact = Consumer('sandwich-maker').has_pact_with(Provider('Butterer'))
  pact.start_service()
  atexit.register(pact.stop_service)

  PACT_BASE_URL = 'http://localhost:1234'

  BREAD_AND_BUTTER = 'bread and butter'

Let's write a test with pact - 2
--------------------------------

.. code:: python


  def test_buttering():

      (pact
      .given('We want to butter bread')
      .upon_receiving('a request to butter bread')
      .with_request('get', '/butter/bread')
      .will_respond_with(200, body=expected_body))

      with pact:
          result = requests.get(f'{PACT_BASE_URL}/butter/bread')

      assert result.text == 'bread and butter'

And run it
----------

.. code:: shell

  $ pytest client1_contract_tests.py
  ============================= test session starts ==============================
  platform darwin -- Python 3.8.6, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
  rootdir: /Users/tibs/Dropbox/talks/pact-talk/examples/client1
  collected 1 item

  client1_contract_tests.py .                                              [100%]

  ============================== 1 passed in 0.75s ===============================

New files
---------

We now have two new files:

``pact-mock-service.log``

``sandwich-maker-butterer.json``

``pact-mock-service.log``
-------------------------

::

  I, [2021-01-08T11:20:52.257590 #13978]  INFO -- : Cleared interactions
  I, [2021-01-08T11:20:52.262320 #13978]  INFO -- : Registered expected interaction GET /butter/bread
  D, [2021-01-08T11:20:52.262556 #13978] DEBUG -- : {
    "description": "a request to butter bread",
    "providerState": "We want to butter bread",
    "request": {
      "method": "get",
      "path": "/butter/bread"
    },
    "response": {
      "status": 200,
      "headers": {
      },
      "body": "bread and butter"
    },
    "metadata": null
  }

continued
---------

::

  I, [2021-01-08T11:20:52.267929 #13978]  INFO -- : Received request GET /butter/bread
  D, [2021-01-08T11:20:52.268008 #13978] DEBUG -- : {
    "path": "/butter/bread",
    "query": "",
    "method": "get",
    "headers": {
      "Host": "localhost:1234",
      "User-Agent": "python-requests/2.25.1",
      "Accept-Encoding": "gzip, deflate",
      "Accept": "*/*",
      "Connection": "keep-alive",
      "Version": "HTTP/1.1"
    }
  }
  I, [2021-01-08T11:20:52.268305 #13978]  INFO -- : Found matching response for GET /butter/bread
  D, [2021-01-08T11:20:52.268405 #13978] DEBUG -- : {
    "status": 200,
    "headers": {
    },
    "body": "bread and butter"
  }
  I, [2021-01-08T11:20:52.273996 #13978]  INFO -- : Verifying - interactions matched
  I, [2021-01-08T11:20:52.278698 #13978]  INFO -- : Writing pact for Butterer to /Users/tibs/Dropbox/talks/pact-talk/examples/client1/sandwich-maker-butterer.json

``sandwich-maker-butterer.json``
--------------------------------

.. code:: json

  {
    "consumer": {
      "name": "sandwich-maker"
    },
    "provider": {
      "name": "Butterer"
    },

continued
---------

.. code:: json

    "interactions": [
      {
        "description": "a request to butter bread",
        "providerState": "We want to butter bread",
        "request": {
          "method": "get",
          "path": "/butter/bread"
        },
        "response": {
          "status": 200,
          "headers": {
          },
          "body": "bread and butter"
        }
      }
    ],

continued
---------

.. code:: json

    "metadata": {
      "pactSpecification": {
        "version": "2.0.0"
      }
    }
  }

Testing the contract against the server
---------------------------------------

With the server running (at ``http://localhost:8080``):

.. code:: shell

  $ pact-verifier \
    --provider-base-url=http://localhost:8080 \
    --pact-url=../client1/sandwich-maker-butterer.json
  INFO: Reading pact at ../client1/sandwich-maker-butterer.json

  Verifying a pact between sandwich-maker and Butterer
    Given We want to butter bread
      a request to butter bread
        with GET /butter/bread
          returns a response which
  WARN: Skipping set up for provider state 'We want to butter bread' ...
            has status code 200
            has a matching body

  1 interaction, 0 failures

Interlude
---------

<music before the next bit>

But buttering should be idempotent
----------------------------------

If we ask to butter the same piece of bread more than once, we still want to
get back "bread and butter".

Idempotent buttering, service2
------------------------------

``service2.py``

.. code:: python

  #!/usr/bin/env python3

  from bottle import Bottle

  app = Bottle()

  @app.route('/butter/<substrate>')
  def butter(substrate):
      if substrate.endswith('butter'):
          return substrate
      else:
          return f'{substrate} and butter'

  if __name__ == '__main__':
      app.run()

A new test for service2
-----------------------

``service2_tests.py``

.. code:: python

  #!/usr/bin/env python3

  from server2 import butter

  def test_butter():
      assert butter('bread') == 'bread and butter'

  def test_already_buttered():
      assert butter('bread and butter') == 'bread and butter'

Our server tests still pass
---------------------------

.. code:: shell

  $ pytest server2_tests.py
  ============================= test session starts ==============================
  platform darwin -- Python 3.8.6, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
  rootdir: /Users/tibs/Dropbox/talks/pact-talk/examples/server2
  collected 2 items

  server2_tests.py ..                                                      [100%]

  ============================== 2 passed in 0.04s ===============================

We still honour the contract with client1
-----------------------------------------

.. code:: shell

  $ pact-verifier \
    --provider-base-url=http://localhost:8080 \
    --pact-url=../client1/sandwich-maker-butterer.json
  INFO: Reading pact at ../client1/sandwich-maker-butterer.json

  Verifying a pact between sandwich-maker and Butterer
    Given We want to butter bread
      a request to butter bread
        with GET /butter/bread
          returns a response which
  WARN: Skipping set up for provider state 'We want to butter bread' ...
            has status code 200
            has a matching body

  1 interaction, 0 failures

And client2 wants to use the new ability
----------------------------------------

An appropriate test against the server would be:

.. code:: python

  def test_buttering_twice():
      result = requests.get(f'{BASE_URL}/butter/bread%20and%20butter')
      assert(result.status_code) == 200
      assert(result.text) == 'bread and butter'

So we add a new contract test
-----------------------------

``client2_contract_tests.py`` - new test

.. code:: python3

  def test_buttering_twice():

      (pact
      .given('We want to butter bread again')
      .upon_receiving('a request to butter buttered bread')
      .with_request('get', '/butter/bread%20and%20butter')
      .will_respond_with(200, body=BREAD_AND_BUTTER))

      with pact:
          result = requests.get(f'{PACT_BASE_URL}/butter/bread%20and%20butter')

      assert result.text == 'bread and butter'

And it passes
-------------

.. code:: shell

  pytest client2_contract_tests.py
  ============================= test session starts ==============================
  platform darwin -- Python 3.8.6, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
  rootdir: /Users/tibs/Dropbox/talks/pact-talk/examples/client2
  collected 2 items

  client2_contract_tests.py ..                                             [100%]

  ============================== 2 passed in 0.79s ===============================

``sandwich-maker-butterer.json``
--------------------------------

A new interaction:

.. code:: json

      {
        "description": "a request to butter buttered bread",
        "providerState": "We want to butter bread again",
        "request": {
          "method": "get",
          "path": "/butter/bread%20and%20butter"
        },
        "response": {
          "status": 200,
          "headers": {
          },
          "body": "bread and butter"
        }
      }
    ],


And service2 is also happy with the new contract
------------------------------------------------

While running service2 at ``http://localhost:8080``

.. code:: shell

  $ pact-verifier \
    --provider-base-url=http://localhost:8080 \
    --pact-url=../client2/sandwich-maker-butterer.json
  INFO: Reading pact at ../client2/sandwich-maker-butterer.json

  Verifying a pact between sandwich-maker and Butterer
    Given We want to butter bread
      a request to butter bread
        with GET /butter/bread
          returns a response which
  WARN: Skipping set up for provider state 'We want to butter bread' ...
            has status code 200
            has a matching body
    Given We want to butter bread again
      a request to butter buttered bread
        with GET /butter/bread%20and%20butter
          returns a response which
  WARN: Skipping set up for provider state 'We want to butter bread again' ...
            has status code 200
            has a matching body

  2 interactions, 0 failures

But the old service and the new contract...
-------------------------------------------

.. code:: shell

  $ pact-verifier \
    --provider-base-url=http://localhost:8080 \
    --pact-url=../client2/sandwich-maker-butterer.json
  INFO: Reading pact at ../client2/sandwich-maker-butterer.json

  Verifying a pact between sandwich-maker and Butterer
    Given We want to butter bread
      a request to butter bread
        with GET /butter/bread
          returns a response which
  WARN: Skipping set up for provider state 'We want to butter bread' ...
            has status code 200
            has a matching body
    Given We want to butter bread again
      a request to butter buttered bread
        with GET /butter/bread%20and%20butter
          returns a response which
  WARN: Skipping set up for provider state 'We want to butter bread again' ...
            has status code 200
            has a matching body (FAILED - 1)

Failures
--------

.. code:: shell

  Failures:

    1) Verifying a pact between sandwich-maker and Butterer Given We want to butter bread
       again a request to butter buttered bread with GET /butter/bread%20and%20butter
       returns a response which has a matching body
      Failure/Error: expect(response_body).to match_term expected_response_body, diff_options, example

        Actual: bread and butter and butter

        Diff
        --------------------------------------
        Key: - is expected
              + is actual
        Matching keys and values are not shown

        -bread and butter
        +bread and butter and butter


Failures
--------

.. code:: shell

        Description of differences
        --------------------------------------
        * Expected "bread and butter" but got "bread and butter and butter" at $

  2 interactions, 1 failure

  Failed interactions:

  PACT_DESCRIPTION='a request to butter buttered bread' PACT_PROVIDER_STATE='We want to
  butter bread again' /Users/tibs/Library/Caches/pypoetry/virtualenvs/pact-talk-zwt4AdHO-py3.8/bin/pact-verifier
  --pact-url=../client2/sandwich-maker-butterer.json --provider-base-url=http://localhost:8080
  # A request to butter buttered bread given We want to butter bread again

Interlude
---------

<music before the next bit>

What if it's not that simple
----------------------------

Let's provide information about the butter being used.

``server3.py`` adds a new route:

.. code:: python

  @app.route('/info')
  def info():
      return {
              'salt': random.choice(['0%', '0.01%']),
              'lactose': random.choice([True, False]),
          }
      )

A new test
----------

In ``server3_tests.py``

.. code:: python

  def test_info():
      result = info()
      assert result['salt'] in ('0%', '0.9%')
      assert result['lactose'] in (True, False)


And in our client
-----------------

A new test in ``client3_tests.py``

.. code:: python

  def test_info():
      result = requests.get(f'{BASE_URL}/info')
      json_result = result.json()
      assert json_result['lactose'] in (True, False)
      salt = json_result['salt']
      assert salt[-1] == '%'
      assert float(salt[:-1]) >= 0.0

Which passes
------------

With server3 running at ``http://localhost:8080``

.. code:: shell

  $ pytest client3_tests.py
  ============================= test session starts ==============================
  platform darwin -- Python 3.8.6, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
  rootdir: /Users/tibs/Dropbox/talks/pact-talk/examples/client3
  collected 3 items

  client3_tests.py ...                                                     [100%]

  ============================== 3 passed in 0.10s ===============================

But we want a contract test
---------------------------

.. code:: python

  from pact import Like, Term

  BUTTER_INFO = Like(
      {
          'salt': Term(r'\d+(\.\d+)?%', '0%'),
          'lactose': False,
      }
  )

And the test
------------

.. code:: python

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

And here is the new interaction
-------------------------------

in ``client3/sandwich-maker-butterer.json``

.. code:: json

    {
      "description": "a request for information",
      "providerState": "We want to know about the butter being used",
      "request": {
        "method": "get",
        "path": "/info"
      },
      "response": {
        "status": 200,
        "headers": {
        },
        "body": {
          "salt": "0%",
          "lactose": false
        },
        "matchingRules": {
          "$.body": {
            "match": "type"
          },
          "$.body.salt": {
            "match": "regex",
            "regex": "\\d+(\\.\\d+)?%"
          }
        }
      }
    }

And the server agrees
---------------------

(with server3 running on ``http://localhost:8080``)

.. code:: shell

  $ pact-verifier \
    --provider-base-url=http://localhost:8080 \
    --pact-url=../client3/sandwich-maker-butterer.json
  INFO: Reading pact at ../client3/sandwich-maker-butterer.json

  Verifying a pact between sandwich-maker and Butterer
    Given We want to butter bread
      a request to butter bread
        with GET /butter/bread
          returns a response which
  WARN: Skipping set up for provider state 'We want to butter bread' ...
            has status code 200
            has a matching body
    Given We want to butter bread again
      a request to butter buttered bread
        with GET /butter/bread%20and%20butter
          returns a response which
  WARN: Skipping set up for provider state 'We want to butter bread again' ...
            has status code 200
            has a matching body
    Given We want to know about the butter being used
      a request for information
        with GET /info
          returns a response which
  WARN: Skipping set up for provider state 'We want to know about ...
            has status code 200
            has a matching body

  3 interactions, 0 failures

Interlude
---------

<music before the next bit>

How to communicate the contract
-------------------------------

Pact broker - run by Pact

Pact broker - run locally

By copying (don't do this?**

Via github or other VCS

Pact 2 versus Pact 3
--------------------

<summary>

Other benefits
--------------

If there is a problem with the API, at either end, you have the stored copy
to look at.

If you're trying to learn what the APIs do, and how they are used, then you
can look at the stored copies. This is sometimes better/simpler than looking
at the tests, which generally aren't written to this purpose.

If your client tests give complete coverage, then the server can tell
exactly which requests that client makes. This can aid in finding dead code,
corresponding to requests that no-one ever makes.

*Anything else?*

Support for multiple programming languages - VCR/Betamax
--------------------------------------------------------

Both VCR and Betamax are "ports" of the Ruby ``vcr`` gem, and they all share
the same storage format.

Support for multiple programming languages - Pact
-------------------------------------------------

Pact has a very active user community, and support for a variety of
programming languages:

  .NET (for C#), Go, JavaScript, Python, Ruby, Rust, the JVM (for Java, Scala,
  Clojure, etc.),

with more in development. And if it is not directly supported for a language,
there are ways around that.

*That means client and server need not be in the same language*

When shouldn't you use Pact
---------------------------

(I love that this is discussed in the Pact documentation)

...

Links for Pact
--------------

* Pact: https://docs.pact.io/

Links for VCR and related
-------------------------

* VCR: https://vcrpy.readthedocs.io/
* Betamax: https://betamax.readthedocs.io/

Tips and tricks on http(s) session recording:
https://medium.com/@george.shuklin/tips-and-tricks-on-http-s-session-recording-4194f99adbf


Fin
---

*Remember, buttering should be idempotent.*

Written in reStructuredText_.

Converted to PDF slides using rst2pdf_.

Source and examples at https://github.com/tibs/pact-talk

|cc-attr-sharealike| This slideshow and its related files are released under a
`Creative Commons Attribution-ShareAlike 4.0 International License`_.

.. |cc-attr-sharealike| image:: images/cc-attribution-sharealike-88x31.png
   :alt: CC-Attribution-ShareAlike image
   :align: middle

.. _`Creative Commons Attribution-ShareAlike 4.0 International License`: http://creativecommons.org/licenses/by-sa/4.0/

.. _CamPUG: https://www.meetup.com/CamPUG/
.. _reStructuredText: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
.. _rst2pdf: https://rst2pdf.org/
