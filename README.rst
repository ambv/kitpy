==========
lck.common
==========

This library consists of various simple common routines and language constructs
that are so useful they ten to be rewritten in every subsequent project I'm
working on. Each function, decorator or module on its own is too simple to
dedicate an entire PyPI package for it.  Together however, this library
represents a Swiss army knife for everyday needs (YMMV). Among the things you
might find inside:

 * robust memoization
   
 * some less obvious collections (e.g. ``orderedset``)

 * a ``@synchronized`` decorator (with threading or lockfile backends)

 * some controversial language enhancements like the Null object

 * converter from ElementTree instances to dicts

 * file finder (searching locations commonly used for storing app data)

The latest version can be installed via `PyPI 
<http://pypi.python.org/pypi/lck.common/>`_::

  $ pip install lck.common
  
or::

  $ easy_install lck.common

The `source code repository <http://github.com/LangaCore/kitpy>`_ and 
`issue tracker <http://github.com/LangaCore/kitpy/issues>`_ are 
maintained on `GitHub <http://github.com/LangaCore/kitpy>`_.

For the curious, ``lck`` stands for LangaCore Kit. LangaCore is a one man
software development shop of mine.

**Note:**  ``lck.common`` requires **Python 2.7** because all of its code is using
the so-called four futures (``absolute_imports``, ``division``, ``print_function``
and ``unicode_literals``). One of the virtues in the creation of this library
is to make the code beautiful. These switches give a useful transitional
state between the old Python 2.x and the new Python 3.x. You should use them as
well.

Change Log
----------

0.4.5
~~~~~

* fixed an uncommon bug in memoization where an exception in the memoized
  function could leave stale keys in the cache 

0.4.4
~~~~~

* ``lck.git`` introduced with a ``get_version`` routine

* ``decode_entities`` added to ``lck.xml``

0.4.3
~~~~~

* ``lck.lang.Null`` introduced, see `Null Object pattern <http://en.wikipedia.org/wiki/Null_Object_pattern>`_

* ``lck.lang.unset`` is now a ``Null`` instance

* ``lck.xml`` introduced with a ``etree_to_dict`` routine

* ``lck.config`` has been removed, use the `configparser backport <http://pypi.python.org/pypi/configparser>`_

0.4.2
~~~~~

* ``lck.crypto`` introduced with a couple of thin wrappers over PyCrypto

* ``lck.math`` introduced starting with Elo rating calculation routine.

0.4.1
~~~~~

* ``lck.lang.unset`` is now also ``False`` and ``len(unset)`` is zero

0.4.0
~~~~~

* migrated to the ``lck`` namespace from ``langacore.kit``

* migrated licensing from GPL 3 to MIT

* bumped the trove from alpha status to beta, the code is in production for over
  a year now

Ancient history
~~~~~~~~~~~~~~~

* No proper change log was kept before 0.4.0
