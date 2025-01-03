import datetime
from unittest.mock import Mock
import numpy as np
import pytest
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.path import Path
from matplotlib.table import CustomCell, Table
from matplotlib.testing.decorators import image_comparison, check_figures_equal
from matplotlib.transforms import Bbox
import matplotlib.units as munits

@image_comparison(['table_zorder.png'], remove_text=True)
def test_zorder_18_mutated():
    data = [[66386, 174296], [58230, 381139]]
    colLabels = ('Freeze', 'Wind')
    rowLabels = ['%d year' % x for x in (100, 50)]
    cellText = []
    yoff = np.zeros(len(colLabels))
    for row in reversed(data):
        yoff += row
        cellText.append(['%1.1f' % (x / 1000.0) for x in yoff])
    t = np.linspace(0, 2 * np.pi, 100)
    plt.plot(t, np.cos(t), lw=4, zorder=2)
    plt.table(cellText=cellText, rowLabels=rowLabels, colLabels=colLabels, loc='center', zorder=-2)
    plt.table(cellText=cellText, rowLabels=rowLabels, colLabels=colLabels, loc='upper center', zorder=4, cellLoc='center')
    plt.yticks([])
# Mutation info: Added cellLoc = center (Call plt.table)