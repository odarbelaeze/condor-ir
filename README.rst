=========
condor-ir
=========

.. image:: https://travis-ci.org/odarbelaeze/condor-ir.svg?branch=master
    :target: https://travis-ci.org/odarbelaeze/condor-ir

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.495722.svg
   :target: https://doi.org/10.5281/zenodo.495722


This is a program to work with examples of Latent Semantic Analysis search
engines, a.k.a., `LSA <https://en.wikipedia.org/wiki/Latent_semantic_analysis>`_.
The program is set up so that it understands froac xml documents on input
as well as plain text records from isi web of knowledge.

You can find more information about froac repositories at
http://froac.manizales.unal.edu.co/froac/ http://froac.manizales.unal.edu.co/froac/
and about isi web of knowledge text files at
`the thomson reuters website <http://images.webofknowledge.com/WOK46/help/WOK/h_ml_options.html>`_

Installing the condor-ir package
----------------------------------

The second thing you will need is to download the program from its pypi
repository,

.. code-block:: bash

  pip install -U condor-ir

the ``-U`` parameter will upgrade the package to the latest version, a very
recommendable step for a unstable package.

For specific databases support you can install their appropriate extra package:

.. code-block:: bash

  pip install -U condor-ir[mysql]
  pip install -U condor-ir[postgres]

Furthermore, we require a bit of the ``nltk`` data package for the stems and
stop word removal to work.

.. code-block:: bash

  python -m nltk.downloader snowball_data stopwords

Finally, in order to prepare the database or reset the database in preparation
for a new version of `condor-ir` you can run the database preparation script,

.. code-block:: bash

  condor utils preparedb

If you need to specify a database other than the default you can do so through
environment variables:

.. code-block:: bash

  export CONDOR_DB_URL="mysql://localhost/condor"
  condor utils preparedb # will now work on mysql://localhost/condor 

CLI Interface
-------------

After installing the program you will have three basic commands at your
disposal, for handling bibliography sets, term document matrices and engines,
the CLI interface gives you most CRUD operations in a hierachical manner.

``condor`` triggers the main program and you can get top level help by running
``condor --help``.

``condor bibliography`` namespaces the bibliography set related commands, you can
list and get help about those using ``condor bibliography --help``.

``condor model`` is a short cut that offers the ``condor model create``
sub command, that creates both a term document matrix and an *lsa* search
engine, get help on *models* using ``condor model --help``.

``condor query <string...>`` this non crud command search a bibliography set
using a previously created search engine, the search engine can be targeted
figure out how using ``condor query --help``.

Feel free to check detailed descriptions of these commands using their
``--help`` flag.
