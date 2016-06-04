# LSA Program

[![Build Status](https://travis-ci.org/odarbelaeze/lsa-program.svg?branch=master)](https://travis-ci.org/odarbelaeze/lsa-program)

[![Documentation Status](https://readthedocs.org/projects/lsa-program/badge/?version=latest)](http://lsa-program.readthedocs.org/en/latest/?badge=latest)

This is a program to work with examples of Latent Semantic Analysis search
engines, a.k.a., [LSA](https://en.wikipedia.org/wiki/Latent_semantic_analysis).
The program is setted up so that it understands froac xml documents on input
as well as plain text reccords from isi web of knowledge.

You can find more information about froac repositories at
[http://froac.manizales.unal.edu.co/froac/](http://froac.manizales.unal.edu.co/froac/)
and about isi web of knowledge text files at
[the thomson reuters website](http://images.webofknowledge.com/WOK46/help/WOK/h_ml_options.html)

## Installing the lsa program package

First of all you will need to get mongodb installed and running in your
system, at the moment the program only works if mongodb is running in the
default port (27017). You can find more information in how to install mongodb
at [https://www.mongodb.org/](https://www.mongodb.org/).

The second thing you will need is to download the program from its pypi
repository,

```bash
pip install -U lsa-program
```

the `-U` parameter will upgrade the package to the latest version, a very
recomendable step for a unstable package.

The language support requires the enchant engine as well as some dictionaries,
for that you can install using your package manager or external tool:

```bash
# Arch
sudo pacman -S enchant aspell-es aspell-en aspell-fr aspell-it aspell-pt
```

```bash
# Ubuntu
sudo apt-get install postgresql postgresql-contrib
sudo apt-get install enchant \
                     aspell-es aspell-en aspell-fr aspell-it aspell-pt
sudo -H -u postgres bash -c 'createuser -s lsaprogram'
sudo -H -u postgres bash -c 'createdb -E UTF-8 -U lsaprogram lsaprogram'
git clone https://github.com/odarbelaeze/lsa-program.git
cd lsa-program
alembic upgrade heads # to create the database schemas

## Seting up your database

After installing the program you will have three basic commands at your
disposal,

Command         | Action
--------------- | -------------------------------------------------------
`lsapopulate`   | populates the mongodb database using files
`lsamodel`      | creates a model for the current records in the database
`lsaquery`      | queries the database using searc terms

Feel free to check detailed descriptions of these commands using their
`--help` flag.
