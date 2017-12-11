# -*- coding: utf-8 -*-

from pkg_resources import resource_filename

try:
    import pytest
except ImportError:
    def test(*args):
        print('tests require `pytest`, and `pytest-mpl`.')

def test(*args):
    options = [resource_filename('template', 'tests')]
    options.extend(list(args))
    return pytest.main(options)

