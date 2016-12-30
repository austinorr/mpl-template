import sys
import matplotlib
import template

matplotlib.use('agg')

status = template.test(*sys.argv[1:])

sys.exit(status)
