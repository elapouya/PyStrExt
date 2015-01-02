.. PyStrExt documentation master file, created by
   sphinx-quickstart on Tue Dec 30 16:11:27 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyStrExt's documentation!
====================================

.. rubric:: Quickstart

To install::
	
	pip install pystrext

Usage::

    >>> import pystrext as strext

    >>> h,m,s = strext.extracts('elapse time : 5h 7m 36s','(\d+)h (\d+)m (\d+)s',['0']*3)
    >>> h,m,s
    ('5', '7', '36')
    ...

.. rubric:: Functions index

.. currentmodule:: pystrext

.. to list all function : grep "def " *.py | sed -e 's,^def ,,' -e 's,(.*,,' | sort
.. autosummary:: 

	MB_GB
	MHz_GHz
	base62_decode
	base62_encode
	compress
	extract
	extracts
	file_unicode
	file_unicode_list
	get_col
	if_val
	is_email_valid
	is_ip_valid
	no_one_many
	plural
	random_password
	remove_accents
	slugify
	truncate
	uncompress
	version_lt
	vjust

.. rubric:: Functions documentation
	
.. automodule:: pystrext
   :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

