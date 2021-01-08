==========================
Contract testing and Pact_
==========================

Written as a talk for CamPUG_

History
~~~~~~~

The talk was (will be) given at CamPUG_ on Tuesday 12th January 2021.

The slides
~~~~~~~~~~
The slides are written using reStructuredText_, and thus intended to be
readable as plain text.

The sources for the slides are in `<pact-slides.rst>`_.

(Note that github will present the ``.rst`` files in rendered form as HTML,
albeit using their own styling (which makes notes a bit odd). If you want
to see the original reStructuredText source, you have to click on the "Raw"
link at the top of the file's page.)

Since this version of the talk uses PDF slides, which I produce via rst2pdf_,
I'm including the resultant PDF files in the repository. These
may not always be as up-to-date as the source files, so check their
timestamps.

* The 4x3 aspect ratio slides are `<pact-slides-4x3.pdf>`_.
* The 16x9 aspect ratio slides are `<pact-slides-16x9.pdf>`_.

Making the PDF files
~~~~~~~~~~~~~~~~~~~~
For convenience, you can use the Makefile to create the PDF slides.
For instance::

  $ make slides

For what the Makefile can do, use::

  $ make help

I use poetry_ to manage the dependencies needed to build the PDFs, and
rst2pdf_ and its dependencies to do the actual work.

.. _poetry: https://python-poetry.org/
.. _rst2pdf: https://rst2pdf.org/

You will also need an appropriate ``make`` program if you want to use the
Makefile.

The examples
~~~~~~~~~~~~

The examples in the slides are all in this repository, in the ``examples``
directory.

They all use bottle_, requests_, pytest_, and pact-python_. The appropriate
dependencies are specified in the top-level ``pyproject.toml``, so (for
instance) doing ``poetry install`` and ``poetry shell`` should get you ready
to run them.

* ``server1`` and ``client1`` have the basic "buttering" endpoint.
* ``server2`` and ``client2`` provide idempotent buttering as well.
* ``server3`` and ``client3`` also provide butter information.

Each directory contains a set of tests, as ``<name>_tests.py_``, and the
client directories also have pact tests, as ``<name>_contract_tests.py``.

.. _CamPUG: https://www.meetup.com/CamPUG/
.. _pandoc: https://pandoc.org/
.. _docutils: http://docutils.sourceforge.net/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _TeX: https://www.ctan.org/starter

.. _pact: https://docs.pact.io/_

.. _bottle: https://bottlepy.org/docs/dev/
.. _requests: https://requests.readthedocs.io/
.. _pytest: https://docs.pytest.org/
.. _pact-python: https://github.com/pact-foundation/pact-python

--------

  |cc-attr-sharealike|

  This slideshow and its related files are released under a `Creative Commons
  Attribution-ShareAlike 4.0 International License`_.

.. |cc-attr-sharealike| image:: images/cc-attribution-sharealike-88x31.png
   :alt: CC-Attribution-ShareAlike image

.. _`Creative Commons Attribution-ShareAlike 4.0 International License`: http://creativecommons.org/licenses/by-sa/4.0/
