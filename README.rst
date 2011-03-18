--------------------
langacore.kit.common
--------------------

This library consists of various simple common routines and language 
constructs that are so useful they ten to be rewritten in every subsequent
project I'm working on. Each function, decorator or module on its own is too
simple to dedicate an entire PyPI package for it.  Together however, this
library represents a Swiss army knife for everyday needs (YMMV). Among the
things you might find inside:

 * robust memoization 
   
 * some less obvious collections (e.g. ``orderedset``)

 * a ``@synchronized`` decorator (with threading or lockfile backends)

 * file finder (searching locations commonly used for storing app data)

The latest version can be installed via `PyPI 
<http://pypi.python.org/pypi/langacore.kit.common/>`_::

  $ pip install langacore.kit.common
  
or::

  $ easy_install langacore.kit.common

The `source code repository <http://github.com/LangaCore/kitpy>`_ and 
`issue tracker <http://github.com/LangaCore/kitpy/issues>`_ are 
maintained on `GitHub <http://github.com/LangaCore/kitpy>`_.

**Note:**  Since 0.2.0 ``langacore.kit.common`` does require **Python 
2.7** because one of the virtues in the creation of this library is to 
make the code beautiful.
