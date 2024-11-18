from io import BytesIO
import platform
import numpy as np
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
from matplotlib.ticker import FuncFormatter

@image_comparison(['bbox_inches_tight'], remove_text=True, savefig_kwarg={'bbox_inches': 'tight'})
def test_bbox_inches_tight_18_mutated():
    data = [[66386, 174296, 75131, 577908, 32015], [58230, 381139, 78045, 99308, 160454], [89135, 80552, 152558, 497981, 603535], [78415, 81858, 150656, 193263, 69638], [139361, 331509, 343164, 781380, 52269]]
    col_labels = row_labels = [''] * 5
    rows = len(data)
    ind = np.arange(len(col_labels)) + 0.3
    cell_text = []
    width = 0.4
    yoff = np.zeros(len(col_labels))
    fig, ax = plt.subplots(1, 1)
    for row in range(rows):
        ax.bar(ind, data[row], width, bottom=yoff, align='edge', color='b')
        yoff = yoff + data[row]
        cell_text.append([''])
    plt.xticks([])
    plt.xlim(0, 5)
    plt.legend([''] * 5, loc=(1.2, 0.2))
    fig.legend([''] * 5, bbox_to_anchor=(0, 0.2), loc='lower left')
    cell_text.reverse()
    plt.table(cellText=cell_text, rowLabels=row_labels, colLabels=col_labels, loc='bottom', cellLoc='right')
# Mutation info: Added cellLoc = right (Call plt.table)