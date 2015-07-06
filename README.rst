Description
===========

An etcd client using tornado's httpclient

Installation
============

This package is stored in PyPI and can be installed the standard way::

    pip install tetcd

The latest release available is:

.. image:: https://badge.fury.io/py/tetcd.png
    :target: http://badbe.fury.io/py/tetcd

Using Tetcd
===========

Usage of this package is documented with sphinx and available at
http://tetcd.readthedocs.org/en/latest/

Developing Tetcd
================

If you would prefer to clone this package directly from git or assist with
development, the URL is https://github.com/kumoru/tetcd.

Tetcd is tested continuously by Travis-CI and running the tests is quite
simple::

    flake8
    nosetests

The current status of the build is:

.. image:: https://secure.travis-ci.org/kumoru/tetcd.png?branch=master
    :target: http://travis-ci.org/kumoru/tetcd

Authors
=======

* Alex Brandt <alunduil@alunduil.com>

Known Issues
============

Known issues can be found in the github issue list at
https://github.com/kumoru/tetcd/issues.

Troubleshooting
===============

If you need to troubleshoot an issue or submit information in a bug report, we
recommend obtaining logs (probably from nose) while enabling log capture of
tetcd.  Tetcd uses logging to submit informational and debug messages but
also sets a NullHandler by default.
