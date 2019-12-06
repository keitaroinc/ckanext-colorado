.. image:: https://travis-ci.org/keitaroinc/ckanext-colorado.svg?branch=master
    :target: https://travis-ci.org/keitaroinc/ckanext-colorado

.. image:: https://coveralls.io/repos/keitaroinc/ckanext-colorado/badge.svg
  :target: https://coveralls.io/r/keitaroinc/ckanext-colorado

.. image:: https://img.shields.io/pypi/v/ckanext-colorado.svg
    :target: https://pypi.org/project/ckanext-colorado/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/ckanext-colorado.svg
    :target: https://pypi.org/project/ckanext-colorado/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/status/ckanext-colorado.svg
    :target: https://pypi.org/project/ckanext-colorado/
    :alt: Development Status

.. image:: https://img.shields.io/pypi/l/ckanext-colorado.svg
    :target: https://pypi.org/project/ckanext-colorado/
    :alt: License

=============
ckanext-colorado
=============

Labor exchange extension for the Colorado CKAN portal.


------------
Requirements
------------

CKAN 2.8.x

------------
Installation
------------

To install ckanext-colorado:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-colorado Python package into your virtual environment::

     pip install ckanext-colorado

3. Add ``colorado`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Replace the SOLR schema with ckanext/colorado/schema.xml
5. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload

---------------
Config settings
---------------

These are the required configuration options used by the extension:

1. Display only organization and tags facets from the defaults
    (mandatory)
    search.facets = organization tags

2. Create dataset without data resource
    (mandatory)
    ckan.dataset.create.require.resource = false



----------------------
Developer installation
----------------------

To install ckanext-colorado for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/keitaroinc/ckanext-colorado.git
    cd ckanext-colorado
    python setup.py develop
    pip install -r dev-requirements.txt


-----
Tests
-----

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.colorado --cover-inclusive --cover-erase --cover-tests


----------------------------------------
Releasing a new version of ckanext-colorado
----------------------------------------

ckanext-colorado should be available on PyPI as https://pypi.org/project/ckanext-colorado.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Make sure you have the latest version of necessary packages::

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version::

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI::

       twine upload dist/*

5. Commit any outstanding changes::

       git commit -a

6. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags
