Decorator modules
-----------------

``@synchronized``
=================
This decorator mimics the behaviour of the Java keyword, enabling users to treat whole
functions or methods as atomic. The most simple use case involves just decorating a function::

  from lck.concurrency import synchronized

  @synchronized
  def func():
    pass

After decoration, all calls to the function are synchronized with a reentrant threading lock
so that no matter how many threads invoke the function at the same time, all calls are
serialized and in effect are run one after another. The default lock is reentrant so it's
okay for a synchronized function to be recursive.

In case where a whole group of functions should be serialized, the user can explicitly provide
a lock object to the decorator::

  from threading import Lock
  from lck.concurrency import synchronized

  LOCK=Lock()

  @synchronized(lock=LOCK)
  def func1():
    pass

  @synchronized(lock=LOCK)
  def func2():
    pass

Sharing a lock means that at any time at most one of the functions in the group is called,
no matter how many threads are running. It's also worth noting that excplicitly providing
a lock enables the user to choose another lock implementation. In the above example a simple
non-reentrant lock is used, in effect the performance is higher than in the reentrant case,
**but the functions sharing the same lock cannot call themselves**.

If the application is run in a multiprocess environment, locks based on threading are not
the answer. In that case the decorator can be fed with a file path instead of a lock object::

  from lck.concurrency import synchronized

  @synchronized(path='/tmp/example.lock')
  def func():
    pass

In that case upon every function call a lock file will be created on the given path to ensure
serial execution across multiple processes. The implementation uses Skip Montanaro's
excellent `lockfile <http://pypi.python.org/pypi/lockfile>`_ library. It is using atomic
operations available on a given platform to ensure correctness. In case of POSIX systems,
hard links are created. On Windows, directories are made.

``@memoize``
============
This decorator enhances performance by storing the outcome of the decorated function
given a specific set of arguments. Across the application the function is called as it
normally would but in fact, only the first call with a concrete set of arguments is calculated.
All subsequent calls with the same arguments return the stored value calculated at first.

This is particularly a win for resource or time consuming functions that are called
multiple times with the same arguments.

The most typical use case for this decorator will be simply::

  from time import sleep
  from lck.cache import memoize

  @memoize
  def expensive_func(arg):
    sleep(10)
    print arg

  expensive_func('Hello') # 10 seconds before we see 'Hello'
  expensive_func('Hello') # now 'Hello' appears instantly 
  expensive_func('World') # 10 seconds before we see 'World'
  expensive_func('World') # now 'World' appears instantly 

The decorator is configurable so that the user can specify how long the outcome should be
cached, or how many different sets of arguments should be stored in the cache::

  from lck.cache import memoize

  @memoize(update_interval=15)
  def recalculation_every_15_seconds():
    pass

  @memoize(max_size=2)
  def only_two_last_used_args_will_be_cached(arg):
    pass

Details
=======
For more detailed view on the decorators, see the documentation below.

.. currentmodule:: lck

.. autosummary::
  :toctree:

  cache.memoization
  concurrency.synchronization
