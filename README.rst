========
PyStrExt
========

This package contains many helper functions to manipulate strings.

Read the fabulous doc `here <http://pystrext.readthedocs.org/en/latest/>`_

Quickstart
==========

To install::
	
	pip install pystrext
	
Usage::

    >>> import pystrext as strext
    >>> h,m,s = strext.extracts('elapse time : 5h 7m 36s','(\d+)h (\d+)m (\d+)s',['0']*3)
    >>> h,m,s
    ('5', '7', '36')
    >>> print strext.no_one_many(0,"No item","One item","%(n)s items")
    No item
    >>> print strext.no_one_many(1,"No item","One item","%(n)s items")
    One item
    >>> print strext.no_one_many(36,"No item","One item","%(n)s items")
    36 items
  	
... more functions available : `read the doc  <http://pystrext.readthedocs.org/en/latest/>`_