import sys

import matplotlib

matplotlib.use('agg')

import template

status = template.test(*sys.argv[1:])

sys.exit(status)
