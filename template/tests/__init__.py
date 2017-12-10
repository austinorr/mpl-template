# -*- coding: utf-8 -*-

from pkg_resources import resource_filename
import pytest

def test(*args):
    options = [resource_filename('template', 'tests')]
    options.extend(list(args))
    return pytest.main(options)

