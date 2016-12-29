from setuptools import find_packages, setup


LONG_DESCRIPTION = """
============
Pinax Forums
============
.. image:: http://slack.pinaxproject.com/badge.svg
   :target: http://slack.pinaxproject.com/

.. image:: https://img.shields.io/travis/pinax/pinax-forums.svg
    :target: https://travis-ci.org/pinax/pinax-forums

.. image:: https://img.shields.io/coveralls/pinax/pinax-forums.svg
    :target: https://coveralls.io/r/pinax/pinax-forums

.. image:: https://img.shields.io/pypi/dm/pinax-forums.svg
    :target:  https://pypi.python.org/pypi/pinax-forums/

.. image:: https://img.shields.io/pypi/v/pinax-forums.svg
    :target:  https://pypi.python.org/pypi/pinax-forums/

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target:  https://pypi.python.org/pypi/pinax-forums/


Pinax
------

Pinax is an open-source platform built on the Django Web Framework. It is an
ecosystem of reusable Django apps, themes, and starter project templates.
This collection can be found at http://pinaxproject.com.

This app was developed as part of the Pinax ecosystem but is just a Django app
and can be used independently of other Pinax apps.


pinax-forums
-------------

``pinax-forums`` is an extensible forums app for Django and Pinax. It is
focused on core forum functionality and hence is expected to be combined with
other Pinax apps for broader features.

See ``pinax-project-forums`` for a full Django project incorporating numerous
apps with the goal of providing an out of the box forums solution.
"""


setup(
    name="pinax-forums",
    version="1.0.0",
    author="Pinax Team",
    author_email="team@pinaxproject.com",
    description="an extensible forum app for Django and Pinax",
    long_description=LONG_DESCRIPTION,
    license="MIT",
    url="http://github.com/pinax/pinax-forums/",
    packages=find_packages(),
    install_requires=[
        "django-appconf>=1.0.1",
        "django-user-accounts==2.0.0"
    ],
    test_suite="runtests.runtests",
    tests_require=[
        "django-appconf>=1.0.1",
        "Django>=1.8",
        "django-user-accounts==2.0.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
