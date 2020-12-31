=========================
Contract testing and Pact
=========================

Written as a talk for CamPUG_

History
~~~~~~~

The talk was given at CamPUG_ on Tuesday 12th January 2021.

The files
~~~~~~~~~
All sources are in reStructuredText_, and thus intended to be readable as
plain text.

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

Making the PDF and HTML files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
For convenience, you can use the Makefile to create the PDF slides, create the
HTML version of the extended notes, and so on. For instance::

  $ make pdf

will make the PDF files.

For what the Makefile can do, use::

  $ make help

Requirements to build the documents:

* I use poetry_ to manage the dependencies needed to build the PDFs.
* rst2pdf_ and its dependencies

.. _poetry: https://python-poetry.org/
.. _rst2pdf: https://rst2pdf.org/

and an appropriate ``make`` program if you want to use the Makefile.

.. _CamPUG: https://www.meetup.com/CamPUG/
.. _pandoc: https://pandoc.org/
.. _docutils: http://docutils.sourceforge.net/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _TeX: https://www.ctan.org/starter

--------

  |cc-attr-sharealike|

  This slideshow and its related files are released under a `Creative Commons
  Attribution-ShareAlike 4.0 International License`_.

.. |cc-attr-sharealike| image:: images/cc-attribution-sharealike-88x31.png
   :alt: CC-Attribution-ShareAlike image

.. _`Creative Commons Attribution-ShareAlike 4.0 International License`: http://creativecommons.org/licenses/by-sa/4.0/
