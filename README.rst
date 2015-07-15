Description
===========

An etcd client using tornado's httpclient

Installation
============

This package is stored in PyPI and can be installed the standard way::

    pip install petcd

The latest release available is:

.. image:: https://badge.fury.io/py/petcd.png
    :target: http://badbe.fury.io/py/petcd

Using petcd
===========

Usage of this package is documented with sphinx and available at
http://petcd.readthedocs.org/en/latest/

Developing petcd
================

If you would prefer to clone this package directly from git or assist with
development, the URL is https://github.com/kumoru/petcd.

petcd is tested continuously by Travis-CI and running the tests is quite
simple::

    flake8
    nosetests

The current status of the build is:

.. image:: https://secure.travis-ci.org/kumoru/petcd.png?branch=master
    :target: http://travis-ci.org/kumoru/petcd

Authors
=======

* Alex Brandt <alunduil@alunduil.com>

Known Issues
============

Known issues can be found in the github issue list at
https://github.com/kumoru/petcd/issues.

Troubleshooting
===============

If you need to troubleshoot an issue or submit information in a bug report, we
recommend obtaining logs (probably from nose) while enabling log capture of
petcd.  petcd uses logging to submit informational and debug messages but
also sets a NullHandler by default.
