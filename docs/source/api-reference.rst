=============
API Reference
=============


**condor-program** main part are the parsers that convert the different kinds
of database documents into manageable dictionaries that only contain the
interest metadata fields. Those are implemented in the :mod:`~condor.record`
module.


The record API
==============

The main class of the record API is the :class:`~condor.record.RecordParser`
class, which outlines an api that parses data out of a raw string, or raw data
structure into a dictionary with the desired interest fields, details about how
to extract that information will go into the
:class:`~condor.record.RecordParser` child classes.


.. autoclass:: condor.record.base.RecordParser
  :members:


Furthermore, the :class:`~condor.record.RecordParser` is complemented by the
:class:`~condor.record.RecordIterator` class, that outlines an interface to
iterate over a file containing several records and returning (yielding) all the
records in a memory efficient fashion.

.. autoclass:: condor.record.base.RecordIterator
  :members:
  :special-members: __iter__


Implementations of the record API
---------------------------------

Parser implementations
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: condor.record.FroacRecordParser
  :members:
  :undoc-members:
  :inherited-members:

.. autoclass:: condor.record.IsiRecordParser
  :members:
  :undoc-members:
  :inherited-members:

.. autoclass:: condor.record.BibtexRecordParser
  :members:
  :undoc-members:
  :inherited-members:

Iterator implementations
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: condor.record.FroacRecordIterator
  :members:
  :undoc-members:
  :inherited-members:

.. autoclass:: condor.record.IsiRecordIterator
  :members:
  :undoc-members:
  :inherited-members:

.. autoclass:: condor.record.BibtexRecordIterator
  :members:
  :undoc-members:
  :inherited-members:


The utility module
==================

.. automodule:: condor.util
  :members:


The scripts package
===================

Database manipulation
---------------------

.. automodule:: condor.dbutil
  :members:

Script entry points
-------------------

The entry points are organized in modules, this leads to some code duplication
but it can be reduced in the future. The populate script, which yields the
`condorpopulate` command is located in the :mod:`~condor.scripts.populate`
module, and contains the information descripted bellow.

.. automodule:: condor.scripts.bibset
  :members:
  :undoc-members:

The model script, which yields the `condormodel` command is located in the
:mod:`~condor.scripts.model` module, and contains the information descripted
bellow.

.. automodule:: condor.scripts.model
  :members:
  :undoc-members:

The query script, which yields the `condorquery` command is located in the
:mod:`~condor.scripts.query` module, and contains the information descripted
bellow.

.. automodule:: condor.scripts.query
  :members:
  :undoc-members:

