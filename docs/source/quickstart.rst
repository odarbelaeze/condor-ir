====================
Quickstart for users
====================

Setup
=====


In order to use the **condor-ir** you need to setup and configure a
**posgresql** database and have it run in the default port as the application
database connection is not yet configurable.

You can also install the **condor-ir** from PyPI using the pip tool

.. code-block:: bash

    $ pip install condor-ir

Furhtermore, for language support you need to install some dictionaries and a
spell checking engine:

.. code-block:: bash

  # Arch
  sudo pacman -S enchant \
                 aspell-es aspell-en aspell-fr aspell-it aspell-pt aspell-de

.. code-block:: bash

  # Ubuntu
  sudo apt-get install enchant \
                       aspell-es aspell-en aspell-fr aspell-it aspell-pt aspell-de

Once you have the mongodb daemon running in your system you can start building
your models using any of the three supported formats:

1. Froac
2. Isi plain text
3. Bibtex

Repository preparation
======================

Once you're done with the setup, you should start preparing your documents to
feed the index database, you can order your sources anyway you want in your
filesystem because the **condor-ir** cli uses a glob matching interface so
you can find the documents you want, an example can be the example repository
provided along with this package:

.. code-block:: bash

  $ tree ../data
  ../data
  +── bib
  │   +── oaa.bib
  +── froac
  │   +── froac1
  │   │   +── 30Algebra relacional. OperaciÃ³n ComposiciÃ³n.xml
  │   │   +── 71Estandares.xml
  │   │   +── 7Programacion lineal.xml
  │   │   +── 83Modelo - Vista - Controlador.xml
  │   │   +── 85Video objeto de aprendizaje CrazyTalk.xml
  │   │   +── 86Aprendiendo con Cuadernia.xml
  │   │   +── 87Introduccion a eXe Learning.xml
  │   │   +── 89OA 1 Clase UTP.xml
  │   │   +── 92Prueba parcial 1.xml
  │   │   +── 97Respuesta libre en circuitos de primer orden.xml
  │   │   +── ...
  │   +── roapManizales1.xml
  │   +── roapManizales2.xml
  │   +── roapManizales3.xml
  │   +── roapManizales4.xml
  │   +── roapManizales5.xml
  +── isi
      +── isi.txt

Populate the database
=====================

Once you have your dataset organized you can populate your database using the
`condorpopulate` program.

.. code-block:: bash

  condor bibset create --xml 'data/*/*.xml'

You can also stipupate a database name and specify if you want to wipe the
database, if you want to combine records from different kinds of databases, you
can do so by reruning the `condorpopulate` tool with the `--no-wipedb` flag,

.. code-block:: bash

  condor bibset create --isi 'data/*/*.isi'
  condor bibset create --bib 'data/*/*.bib'

However, whenever using this approximation, beaware of the record duplication
as the hashing algorithms used to detect duplicates are different for the
different kinds of record files.

Build a model for the database
==============================

Once your database is populated you can build a model or ranking matrix for
your database using the command:

.. code-block:: bash

  condor model

This program will create versioned models so that you can build different
versions, or query with one model when another one is still being built.

Beaware that this is the most time consuming operation in the suite as it
involves inverting a several thousand rank matrix.

Query the model
===============

Once you have built the model you can start performing queries, you can do
so by:

.. code-block:: bash

  condor query search terms

This will perform a query to the latest available model in the model database.

Next steps
==========

1. Learn more about latent semantic analysis
2. Learn more about index databases
3. Learn more about the different supported fileformats
