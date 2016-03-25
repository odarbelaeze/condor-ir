====================
Developer quickstart
====================


**lsa-program** is a free and open source software, contributions are very
wellcome and you can start contributing through the common *github* pattern.


Setting up the development environment
======================================

First you need to clone the repository:

.. code-block:: bash

  git clone https://github.com/odarbelaeze/lsa-program.git
  # Alternatively you can fork and clone your own fork
  git clone https://github.com/<username>/lsa-program.git

Then the most recomendable way for you to do development is in a virtual
environment, we will assume that you are familiar with *virtualenvwrapper*

.. code-block:: bash

  cd lsa-program
  mkvirtualenv -a $PWD -p $(which python3) -r piprequirements.txt lsaenv
  pip install -e .  # This command will also install dependencies


Running tests
=============

When contributing to an open source project, it's crucial that you are able to
run its test suite, this project suggests pytest as testing framework and you
can use its test runner to run our tests, in order to run our test you need to
install testing dependencies, you can do so automatically using the `setup.py`
script

.. code-block:: bash

  python setup.py test


Otherwise, you could manually install the testing dependencies and run tests
manually,

.. code-block:: bash

  pip install pytest
  python -m pytest

Furthermore, you can install pytest plugins such as **coverage** via the
**pytest-cov** plugin and run the test suite using their custom flags.


Contributing to the code
========================

What you can contribute
-----------------------

You can contribute to the code, not only by adding new features and smashing
yourself to the keyboard at the core of the program, some examples of
contributions you can make are the following:

+ Write documentation
+ Write tests, maybe while you are trying to understand what the code does
+ Refactor code, here and there there are optimizations that can be made

Otherwise, you can expand the funcionality of th erecord parsers by adding
support for more document kinds.

How to contribute
-----------------

This project supports the feature branch and pull request (PR) way of doing
contributions through git, you start by adding a new branch to your repo,

.. code-block:: bash

  # While in the repo folder
  git checkout -b <a-name-that-outlines-your-contribution>
  # Do some ground work
  git push -u <origin> <a-name-that-outlines-your-contribution>

Then you proced to create the pull request in github, right away, so you
can start communicating with the core developers and other members of the
community.

Recomendations and code guidelines
----------------------------------

Honoring code guidelines is a key part of contributing to a project, that's
because fixing indentation and correcting line lengths is assumed by git as a
rewrite, and the authorship of the contributed code might be diluted.  This
project includes a `.editorconfig` file that can be used by modern text editors
to automatically keep coding guidelines for different filetypes.

Although the code coverage of this project might be low at some point,
contributors are encouraged to write tests for their features, and also,
regression tests for the code that is already there. Test are writen using
**pytest** which is a very easy to use testing framework, to start you just
need to drop a function whos name starts with `test_` into one module within
the `tests` folder, and the suite will automatically pick up your testing code.
