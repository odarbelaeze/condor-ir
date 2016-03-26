=============
API Reference
=============


**lsa-program** main part are the parsers that convert the different kinds of
database documents into manageable dictionaries that only contain the interest
metadata fields. Those are implemented in the :mod:`~lsa.record` module.


The record API
==============

The main class of the record API is the :class:`~lsa.record.RecordParser`
class, which outlines an api that parses data out of a raw string, or raw data
structure into a dictionary with the desired interest fields, details about how
to extract that information will go into the :class:`~lsa.record.RecordParser`
child classes.


.. autoclass:: lsa.record.RecordParser
  :members:


Furthermore, the :class:`~lsa.record.RecordParser` is complemented by the
:class:`~lsa.record.RecordIterator` class, that outlines an interface to iterate
over a file containing several records and returning (yielding) all the
records in a memory efficient fashion.

.. autoclass:: lsa.record.RecordIterator
  :members:
  :special-members: __iter__


Implementations of the record API
---------------------------------

Parser implementations
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: lsa.record.FroacRecordParser
  :members:
  :undoc-members:
  :inherited-members:

.. autoclass:: lsa.record.IsiRecordParser
  :members:
  :undoc-members:
  :inherited-members:

.. autoclass:: lsa.record.BibtexRecordParser
  :members:
  :undoc-members:
  :inherited-members:

Iterator implementations
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: lsa.record.FroacRecordIterator
  :members:
  :undoc-members:
  :inherited-members:

.. autoclass:: lsa.record.IsiRecordIterator
  :members:
  :undoc-members:
  :inherited-members:

.. autoclass:: lsa.record.BibtexRecordIterator
  :members:
  :undoc-members:
  :inherited-members:


The utility module
==================

.. automodule:: lsa.util
  :members:


The scripts package
===================

Database manipulation
---------------------

.. automodule:: lsa.scripts.dbutil
  :members:

Script entry points
-------------------

The entry points are organized in modules, this leads to some code duplication
but it can be reduced in the future. The populate script, which yields the
`lsapopulate` command is located in the :mod:`~lsa.scripts.populate` module,
and contains the information descripted bellow.

.. automodule:: lsa.scripts.populate
  :members:

.. autofunction:: lsa.scripts.populate.lsapopulate

The model script, which yields the `lsamodel` command is located in the
:mod:`~lsa.scripts.model` module, and contains the information descripted
bellow.

.. automodule:: lsa.scripts.model
  :members:

.. autofunction:: lsa.scripts.model.lsamodel

The query script, which yields the `lsaquery` command is located in the
:mod:`~lsa.scripts.query` module, and contains the information descripted
bellow.

.. automodule:: lsa.scripts.query
  :members:

.. autofunction:: lsa.scripts.query.lsaquery

