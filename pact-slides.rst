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

  SERVER_BASE_URL = 'http://localhost:8080/butter'

  def test_buttering():
      result = requests.get(f'{SERVER_BASE_URL}/bread')
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

Getting a recording
-------------------

<show how to do that>

.. code:: shell

   ...

The Pact recording
------------------

<show the resultant file>

And using it
------------

<and how to amend the test to use it>

``client1_contract_tests.py``

.. code:: python

   ...

But it's also a contract...
---------------------------

``service1_contract_tests.py``

.. code:: python

   ...

Which we can test is honoured by our service
--------------------------------------------

<show testing that the service honours the contract>

.. code:: shell

   ...

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

And add a new test for service2
-------------------------------

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

For what it's worth, we still honour the contract
-------------------------------------------------

.. code:: shell

   ...

And client2 wants to use the new ability
----------------------------------------

``client2_contract_tests.py``

<make this code correct>

.. code:: python

  #!/usr/bin/env python3

  import requests

  def test_buttering():
      result = requests.get(f'{SERVER_BASE_URL}/bread')
      assert(result.status_code) == 200
      assert(result.text) == 'bread and butter'

  def test_buttering_twice():
      result = requests.get(f'{SERVER_BASE_URL}/bread%20and%20butter')
      assert(result.status_code) == 200
      assert(result.text) == 'bread and butter'

But it fails!
-------------

<show the failure>

.. code:: shell

...because the contract (the recording) doesn't know this new functionality

Although if we use the server directly
--------------------------------------

Remember the test against the server? We can extend it.

``client2_tests.py``

.. code:: python

  #!/usr/bin/env python3

  import requests

  SERVER_BASE_URL = 'http://localhost:8080/butter'

  def test_buttering():
      result = requests.get(f'{SERVER_BASE_URL}/bread')
      assert(result.status_code) == 200
      assert(result.text) == 'bread and butter'

  def test_buttering_twice():
      result = requests.get(f'{SERVER_BASE_URL}/bread%20and%20butter')
      assert(result.status_code) == 200
      assert(result.text) == 'bread and butter'

Those tests pass
----------------

.. code:: shell

  $ pytest client2_tests.py
  ============================= test session starts ==============================
  platform darwin -- Python 3.8.6, pytest-6.2.1, py-1.10.0, pluggy-0.13.1
  rootdir: /Users/tibs/Dropbox/talks/pact-talk/examples/client2
  collected 2 items

  client2_tests.py ..                                                      [100%]

  ============================== 2 passed in 0.11s ===============================

(assuming I rememeber to run the corresponding server)

So we need to update the contract
---------------------------------

Show how.

.. code:: shell

   ...

And now client2 is happy with the contract
------------------------------------------

<do I need a slide before this for a different ``client2_contract_tests.py``?>

<show it>

.. code:: shell

   ...


And the new service is happy with the contract
----------------------------------------------

.. code:: shell

   ...

But the old service and the new contract...
-------------------------------------------

.. code:: shell

   ...

Combinations
------------

Have I got this right?

  client1, old contract: OK

  client1, new contract: OK

  client2, old contract: no

  client2, new contract: OK

and
---

  service1, old contract: OK

  service1, new contract: no

  service2, old contract: OK

  service2, new contract: OK


Interlude
---------

<music before the next bit>

How to communicate the contract
-------------------------------

Pact broker - run by Pact

Pact broker - run locally

By copying (don't do this?**

Via github or other VCS

Interlude
---------

<music before the next bit>

Examples of more complicated contracts
--------------------------------------

Choices / inexact matches / approximations

A more complex contract: example data
-------------------------------------

**Convert to Python!**

.. code:: ruby

  # This is a fairly minimal legal example, as determined by experimentation
  # In particular, the "top level" type must be from a known enumeration,
  # and the "second level" type is also limited to particular values.
  example_data = [
    {
      name: 'Something',
      type: 'Sometype',
      settings: [
        {
          name: 'label',
          label: 'Test label'
        }
      ]
    }
  ]

A more complex contract: example test
-------------------------------------

**Convert to Python!**

.. code:: ruby

  describe 'a request to get metadata for settings' do
    it 'gets the expected metadata' do
       our_server.upon_receiving('a metadata request')
        .with(method: :get, path: '/v1/our_server/metadata',
              query: 'tell_me=settings')
        .will_respond_with(
           status: 200,
           headers: {'Content-Type' => 'application/json; charset=utf- 8'},
           body: each_like(
             name: like('Something'),
             type: like('Sometype'),
             settings: each_like( name: 'label', label: 'Test label')
           )
        )
    end
  end

A more complex contract: the contract - 1
-----------------------------------------

.. code:: json

  {
      "consumer": {
          "name": "our-client"
      },
      "provider": {
          "name": "our-server"
      },

A more complex contract: the contract - 2
-----------------------------------------

.. code:: json

      "interactions": [
          {
              "description": "a metadata request",
              "request": {
                  "method": "get",
                  "path": "/v1/our_service/metadata",
                  "query": "tell_me=settings"
              },

A more complex contract: the contract - 3
-----------------------------------------

.. code:: json

              "response": {
                  "status": 200,
                  "headers": {
                      "Content-Type": "application/json; charset=utf-8"
                  },
                  "body": [
                      {
                          "name": "Something",
                          "type": "Sometype",
                          "settings": [
                              { "value1": "happy", "value2": "round" }
                          ]
                      }
                  ],

A more complex contract: the contract - 4
-----------------------------------------

.. code:: json

                  "matchingRules": {
                      "$.body": { "min": 1 },
                      "$.body[*].*": { "match": "type" },
                      "$.body[*].name": { "match": "type" },
                      "$.body[*].type": { "match": "type" },
                      "$.body[*].settings": { "min": 1 },
                      "$.body[*].settings[*].*": { "match": "type" }
                  }
              },
              "metadata": null
          }
      ],

A more complex contract: the contract - 5
-----------------------------------------

.. code:: json

      "metadata": {
          "pactSpecification": { "version": "2.0.0"}
      }
  }


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

Source and extended notes at https://github.com/tibs/pact-talk

|cc-attr-sharealike| This slideshow and its related files are released under a
`Creative Commons Attribution-ShareAlike 4.0 International License`_.

.. |cc-attr-sharealike| image:: images/cc-attribution-sharealike-88x31.png
   :alt: CC-Attribution-ShareAlike image
   :align: middle

.. _`Creative Commons Attribution-ShareAlike 4.0 International License`: http://creativecommons.org/licenses/by-sa/4.0/

.. _CamPUG: https://www.meetup.com/CamPUG/
.. _reStructuredText: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html
.. _rst2pdf: https://rst2pdf.org/
