========================================
Notes on Python and Pact - trying it out
========================================

The Pact documentation (at
https://docs.pact.io/implementation_guides/python/readme)
suggests that the preferred/supported Python impementation is
pact-python_

This is a Pact 2 implementation, at least at the moment.

The other implementation (Pactman_) is not officially supported, and does not
appear to be in active development.

.. _pact_python: https://github.com/pact-foundation/pact-python/
.. _pactman: https://github.com/reecetech/pactman_

https://docs.pact.io/implementation_guides/python/readme is "How to use
pact-python", starting with installation and working through its example
end-to-end examples, which are at
https://github.com/pact-foundation/pact-python/tree/master/examples/e2e

So let's try it...

I'll use Python 3.8.6 as that's been around a while (pyenv also has 3.9.0, but
not yet 3.9.1)

.. note:: It's ``pyenv install --list`` to see what versions are
   available to install!

.. code:: shell

   $ pyenv install 3.8.6
   $ cd ~/talks/pact-talk
   $ pyenv local 3.8.6
   $ poetry install      # to install my slide making environment

That's given me a Python 3.8.6 virtual environment, so use it:

.. code:: shell

   $ poetry shell

.. code:: shell

   $ cd examples

Let's get the e2e example locally...

.. code:: shell

   $ git clone git@github.com:pact-foundation/pact-python.git

and add that ``examples/pact-python`` to my ``.gitignore`` file.

The ``requirements.txt`` in the ``pact-python/examples/e2e`` directory tells
me what else I need. Let's follow the instructions.

I'm already in my poetry virtual environment, so I can do:

.. code:: shell

   $ cd python-pact/examples/e2e
   $ pip install -r requirements.txt
   $ pip install ../../

.. note:: Be careful not to do ``pip install pact-python`` before the other
   ``pip install`` commands. The last command above runs the ``setup.py`` in
   the top-level directory, which itself installs pact-python. It doesn't work
   if it's already installed.

So let's try:

.. code:: shell

   $ pytest

which fails. In summary::

    2 interactions, 2 failures

    Failed interactions:

    PACT_DESCRIPTION='a request for UserA' PACT_PROVIDER_STATE='UserA exists and is not an administrator' /Users/tibs/Library/Caches/pypoetry/virtualenvs/pact-talk-zwt4AdHO-py3.8/bin/pytest # A request for usera given UserA exists and is not an administrator
    PACT_DESCRIPTION='a request for UserA' PACT_PROVIDER_STATE='UserA does not exist' /Users/tibs/Library/Caches/pypoetry/virtualenvs/pact-talk-zwt4AdHO-py3.8/bin/pytest # A request for usera given UserA does not exist

which I *assume* is not intended?

Although it's not clear - this *is* what I'd expect if I needed the local
broker to be running, as described in the next paragaraph.

So let's install docker-compose (yes, I know it's somewhat non-standard to use
homebrew for this, but it's an experiment).

.. code:: shell

   $ brew install docker-compose

and start the application (in ``/Applications``) by hand (which also finishes
the installation).

Then I can do:

.. code:: shell

   $ # in a new window
   $ cd ~/talks/pact-talk
   $ poetry shell
   $ cd examples/pact-python/examples/broker/
   $ docker-compose up

If I go to ``http://localhost`` then I get a login prompt. So that's
presumably working.

But I still get 1 failed test if I run ``pytest`` in my e2e directory
(2 failed interactions)::

    PACT_DESCRIPTION='a request for UserA' PACT_PROVIDER_STATE='UserA exists and is not an administrator' /Users/tibs/Library/Caches/pypoetry/virtualenvs/pact-talk-zwt4AdHO-py3.8/bin/pytest # A request for usera given UserA exists and is not an administrator
    PACT_DESCRIPTION='a request for UserA' PACT_PROVIDER_STATE='UserA does not exist' /Users/tibs/Library/Caches/pypoetry/virtualenvs/pact-talk-zwt4AdHO-py3.8/bin/pytest # A request for usera given UserA does not exist

Next: go back and read through the Python example in the Pact documentation,
to see if that helps.



(If I was doing this from scratch myself, I'd have been tempted to use bottle
instead of flask, but let's go with what we've got.)



======
Take 2
======

::

  $ cd ~/talks/pact-talk
  $ rm -rf ~/Library/Caches/pypoetry/
  $ poetry install
  $ poetry shell
  $ poetry add bottle requests pytest
  $ cd examples

So first our simple buttering service, in the ``server1/`` directory.
