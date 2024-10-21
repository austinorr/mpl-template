# `mpl-template`
A python class for creating full report figures, including borders, titleblocks, logos, and content, entirely within matplotlib.

[![Build Status](https://github.com/austinorr/mpl-template/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/austinorr/mpl-template/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/austinorr/mpl-template/branch/master/graph/badge.svg)](https://codecov.io/gh/austinorr/mpl-template)

[Docs](https://austinorr.github.io/mpl-template/)

## Quick start

Simply importing `mpl_template` lets you use the report template module.

```python
import matplotlib as mpl
from mpl_template import template
import math

report_fig = template.Template(figsize=(8.5, 11), draft=True, scriptname='template.py')

title_block = [
    {
        'name': 'title',
        'text': {
            's': 'Example Figure',
            'x': 0.5,
            'y': 0.5,
            'va': 'center',
            'ha': 'center',
        }
    },
    {},{},{},{},
]
report_fig.titleblock_content = title_block
report_fig.path_text = 'template.py'
fig = report_fig.setup_figure()
page_ax = report_fig.add_page()

# create a sub-gridspec that will be used for the main image
left, right, top, bottom = report_fig.margins
main = report_fig.gsfig[4 + top:-(report_fig.t_h + bottom + 8), 8 + left:-(right + 8)]
gs_timeseries = mpl.gridspec.GridSpecFromSubplotSpec(3, 1, main, hspace=0.3, wspace=0.3)

for n in range(3):
    ax = fig.add_subplot(gs_timeseries[n])
    ax.set_ylim(-2.5, 2.5)
    plot = ax.plot([math.sin(i * (n + 1)) for i in range(0, 100)])
```

![Example Report Document](https://raw.githubusercontent.com/austinorr/mpl-template/refs/heads/main/sphinx_docs/source/img/quick_start_mpl_template.png "Example Report Document")

## Installation
### Dependencies
requires: `matplotlib`
optional: `pillow`, `requests`
tests: `pytest`, `pytest-mpl`, `pytest-cov`

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
Testing is done via `pytest`:
`$pytest --mpl`
