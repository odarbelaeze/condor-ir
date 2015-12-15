# LSA Program

This is a program to work with examples of Latent Semantic Analysis search
engines, a.k.a., [LSA](https://en.wikipedia.org/wiki/Latent_semantic_analysis).
the program is setted up so that it understands froac xml documents on input
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
