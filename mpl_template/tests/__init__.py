# -*- coding: utf-8 -*-

from pkg_resources import resource_filename

try:
    import pytest
    def test(*args):
        options = [resource_filename('mpl_template', 'tests')]
        options.extend(list(args))
        return pytest.main(options)

except ImportError:
    def test(*args):
        print('tests require `pytest`, and `pytest-mpl`.')



