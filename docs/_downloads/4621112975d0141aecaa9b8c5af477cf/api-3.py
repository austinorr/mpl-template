import matplotlib.pyplot as plt
from mpl_template import insert_image

file = "img/polar_bar_demo.png"
fig, ax = plt.subplots(figsize=(3, 3))
img_ax = insert_image(ax, file, scale=2, expand=True)
