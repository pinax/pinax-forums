![](http://pinaxproject.com/pinax-design/patches/pinax-forums.svg)

# Pinax Forums

[![](https://img.shields.io/pypi/v/pinax-forums.svg)](https://pypi.python.org/pypi/pinax-forums/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-forums.svg)](https://circleci.com/gh/pinax/pinax-forums)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-forums.svg)](https://codecov.io/gh/pinax/pinax-forums)
[![](https://img.shields.io/github/contributors/pinax/pinax-forums.svg)](https://github.com/pinax/pinax-forums/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-forums.svg)](https://github.com/pinax/pinax-forums/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-forums.svg)](https://github.com/pinax/pinax-forums/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


## Table of Contents

* [About Pinax](#about-pinax)
* [Important Links](#important-links)
* [Overview](#overview)
  * [Supported Django and Python Versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Settings](#settings)
  * [Templates](#templates)  
* [Change Log](#change-log)
* [History](#history)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable
Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.


## Important Links

Where you can find what you need:
* Releases: published to [PyPI](https://pypi.org/search/?q=pinax) or tagged in app repos in the [Pinax GitHub organization](https://github.com/pinax/)
* Global documentation: [Pinax documentation website](https://pinaxproject.com/pinax/)
* App specific documentation: app repos in the [Pinax GitHub organization](https://github.com/pinax/)
* Support information: [SUPPORT.md](https://github.com/pinax/.github/blob/master/SUPPORT.md) file in the [Pinax default community health file repo](https://github.com/pinax/.github/)
* Contributing information: [CONTRIBUTING.md](https://github.com/pinax/.github/blob/master/CONTRIBUTING.md) file in the [Pinax default community health file repo](https://github.com/pinax/.github/)
* Current and historical release docs: [Pinax Wiki](https://github.com/pinax/pinax/wiki/)


## pinax-forums

### Overview

`pinax-forums` is an extensible forums app for Django and Pinax. It is focused
on core forum functionality and hence is expected to be combined with other
Pinax apps for broader features.

#### Supported Django and Python Versions

Django / Python | 3.6 | 3.7 | 3.8
--------------- | --- | --- | ---
2.2  |  *  |  *  |  *
3.0  |  *  |  *  |  *


## Documentation

### Installation

To install pinax-forums:

```shell
$ pip install pinax-forums
```

Add `pinax.forums` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    # other apps
    "pinax.forums",
]
```

Add `pinax.forums.urls` to your project urlpatterns:

```python
urlpatterns = [
    # other urls
    url(r"^forums/", include("pinax.forums.urls", namespace="pinax_forums")),
]
```

### Settings

#### PINAX_FORUMS_EDIT_TIMEOUT

Allow changes for up to `PINAX_FORUMS_EDIT_TIMEOUT` seconds after creating a post.
Once this period has expired the post is no longer editable.

#### PINAX_FORUMS_HOOKSET

### Templates

The templates referenced by pinax-forums code must be supplied by the user.
Place template files in a `pinax/forums/` subfolder in your project template search path.

#### `category.html`

#### `forum.html`

#### `forums.html`

#### `post_create.html`

#### `post_edit.html`

#### `reply_create.html`

#### `subscribe.html`

#### `thread.html`

#### `thread_updates.html`

#### `unsubscribe.html`


## Change Log

### 2.0.0

* Drop Django 1.11, 2.0, and 2.1, and Python 2,7, 3.4, and 3.5 support
* Add Django 2.2 and 3.0, and Python 3.6, 3.7, and 3.8 support
* Update packaging configs
* Direct users to community resources

### 1.0.2

* Allow use with any account-management package by removing django-user-accounts dependency

### 1.0.1

* Add django>=1.11 to installation requirements
* Update CI configuration
* Delete unused files
* Update documentation
* Fix license target link

### 1.0.0

* Add Django 2.0 compatibility testing
* Drop Django 1.8, 1.9, 1.10, and Python 3.3 support
* Move documentation into README and standardize layout
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description


## History

`pinax-forums` was originally built by [Eldarion](http://eldarion.com) and
called `agora`. It incorporates code and ideas from various client projects.
The clients were kind enough to allow Eldarion to open source the app and
contribute it to Pinax.


## Contribute

[Contributing](https://github.com/pinax/.github/blob/master/CONTRIBUTING.md) information can be found in the [Pinax community health file repo](https://github.com/pinax/.github).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a [Code of Conduct](https://github.com/pinax/.github/blob/master/CODE_OF_CONDUCT.md). We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject) and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-present James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).
