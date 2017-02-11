========
condor-ir
========

Access to roadmap here: `roadmap <https://www.lucidchart.com/invitations/accept/61d72a6b-d843-42b5-b54a-22c7f85e84d3>`_.

.. image:: https://travis-ci.org/odarbelaeze/condor-ir.svg?branch=master
    :target: https://travis-ci.org/odarbelaeze/condor-ir

.. image:: https://readthedocs.org/projects/condor-ir/badge/?version=latest
    :target: (http://condor-ir.readthedocs.org/en/latest/?badge=latest



This is a program to work with examples of Latent Semantic Analysis search
engines, a.k.a., `LSA <https://en.wikipedia.org/wiki/Latent_semantic_analysis>`_.
The program is setted up so that it understands froac xml documents on input
as well as plain text reccords from isi web of knowledge.

You can find more information about froac repositories at
http://froac.manizales.unal.edu.co/froac/ http://froac.manizales.unal.edu.co/froac/
and about isi web of knowledge text files at
`the thomson reuters website <http://images.webofknowledge.com/WOK46/help/WOK/h_ml_options.html>`_

Installing the condor-ir package
----------------------------------

The second thing you will need is to download the program from its pypi
repository,

.. code-block:: bash

  pip install -U condor-ir==1.0.0b7

the `-U` parameter will upgrade the package to the latest version, a very
recomendable step for a unstable package.

The language support requires the enchant engine as well as some dictionaries,
for that you can install using your package manager or external tool:

.. code-block:: bash

  # Arch
  sudo pacman -S enchant \
                 aspell-es aspell-en aspell-fr \
                 aspell-it aspell-pt aspell-de

.. code-block:: bash

  # Ubuntu
  sudo apt-get install enchant \
                       aspell-es aspell-en aspell-fr \
                       aspell-it aspell-pt aspell-de

Setup database and schemas
--------------------------

.. code-block:: bash

  condor utils preparedb


CLI Interface
-------------

After installing the program you will have three basic commands at your
disposal, for handling bibliography sets, term document matrices and engines,
the CLI interface gives you most CRUD operations in a hierachical manner.

``condor`` triggers the main program and you can get top level help by running
``condor --help``.

``condor bibset`` namespaces the bibliography set related commands, you can
list and get help about those using ``condor bibset --help``.

``condor model`` is a short cut that offers the ``condor model create``
subcommand, that chreates both a term document matrix and an *lsa* search
engine, get help on *models* using ``condor model --help``.

``condor query <string...>`` this non crud command search a bibliography set
using a previously created search engine, the search engine can be targeted
figure out how using ``condor query --help``.

Feel free to check detailed descriptions of these commands using their
``--help`` flag.
