========
CondorIR
========

Access to roadmap here: `roadmap <https://www.lucidchart.com/invitations/accept/61d72a6b-d843-42b5-b54a-22c7f85e84d3>`_.

.. image:: https://travis-ci.org/odarbelaeze/lsa-program.svg?branch=master
    :target: https://travis-ci.org/odarbelaeze/lsa-program

.. image:: https://readthedocs.org/projects/lsa-program/badge/?version=latest
    :target: (http://lsa-program.readthedocs.org/en/latest/?badge=latest



This is a program to work with examples of Latent Semantic Analysis search
engines, a.k.a., `LSA <https://en.wikipedia.org/wiki/Latent_semantic_analysis>`_.
The program is setted up so that it understands froac xml documents on input
as well as plain text reccords from isi web of knowledge.

You can find more information about froac repositories at
http://froac.manizales.unal.edu.co/froac/ http://froac.manizales.unal.edu.co/froac/
and about isi web of knowledge text files at
`the thomson reuters website <http://images.webofknowledge.com/WOK46/help/WOK/h_ml_options.html>`_

Installing the CondorIR package
----------------------------------

First of all you will need to get mongodb installed and running in your system,
at the moment the program only works if postgresql is running on your system,
you also need to have a database and a database user for the program.

The second thing you will need is to download the program from its pypi
repository,

.. code-block:: bash

    pip install -U condorir

the `-U` parameter will upgrade the package to the latest version, a very
recomendable step for a unstable package.

The language support requires the enchant engine as well as some dictionaries,
for that you can install using your package manager or external tool:

.. code-block:: bash

    # Arch
    sudo pacman -S postgresql
    sudo pacman -S enchant aspell-es aspell-en aspell-fr aspell-it aspell-pt
    sudo service start postgresql.service # You might want to enable as well
    git clone https://github.com/odarbelaeze/condorir.git
    sudo -H -u postgres bash -c 'createuser -s condorir'
    sudo -H -u postgres bash -c 'createdb -E UTF-8 -U condorir condorir'
    cd condorir
    alembic upgrade heads # to create the database schemas

.. code-block:: bash

    # Ubuntu
    sudo apt-get install postgresql postgresql-contrib
    sudo apt-get install enchant \
                     aspell-es aspell-en aspell-fr aspell-it aspell-pt
    sudo -H -u postgres bash -c 'createuser -s condorir'
    sudo -H -u postgres bash -c 'createdb -E UTF-8 -U condorir condorir'
    git clone https://github.com/odarbelaeze/condorir.git
    cd condorir
    alembic upgrade heads # to create the database schemas


Seting up your database
-----------------------

After installing the program you will have three basic commands at your
disposal,

+---------------------+---------------------------------------------------------+
| Command             | Action                                                  |
+=====================+=========================================================+
| ``condorpopulate``  | populates the mongodb database using files              |
+---------------------+---------------------------------------------------------+
| ``condormodel``     | creates a model for the current records in the database |
+---------------------+---------------------------------------------------------+
| ``condorquery``     | queries the database using searc terms                  |
+---------------------+---------------------------------------------------------+

Feel free to check detailed descriptions of these commands using their ``--help`` flag.