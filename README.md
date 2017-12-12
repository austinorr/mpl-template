# `mpl-template`
A python class for creating full report figures, including borders, titleblocks, logos, and content, entirely within matplotlib.

[![Build Status](https://travis-ci.org/austinorr/mpl-template.svg)](https://travis-ci.org/austinorr/mpl-template)
[![codecov](https://codecov.io/gh/austinorr/mpl-template/branch/master/graph/badge.svg)](https://codecov.io/gh/austinorr/mpl-template)

[Sphinx Docs](https://austinorr.github.io/mpl-template/)

## Installation
### Dependencies
requires: `matplotlib`
optional: `pillow`, `requests`
tests: `pytest`, `pytest-mpl`

### Official Releases
TODO: release on pypi
For now, please install from source.

### Development Builds
This is a pure-python package, so building from source is easy on all platforms:
```
git clone https://github.com/austinorr/mpl-template.git
cd mpl-template
pip install -e .
```
### Testing
Testing is done via the `pytest` module from within the package directory.
`$python check_mpl_template.py --mpl`
or
`$pytest --mpl`
