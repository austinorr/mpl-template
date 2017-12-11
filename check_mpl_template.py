import sys
import matplotlib
matplotlib.use('agg')

import mpl_template

status = mpl_template.test(*sys.argv[1:])

sys.exit(status)
