import datetime
import platform
import re
from unittest import mock
import contourpy
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_almost_equal_nulp
import matplotlib as mpl
from matplotlib import pyplot as plt, rc_context, ticker
from matplotlib.colors import LogNorm, same_color
import matplotlib.patches as mpatches
from matplotlib.testing.decorators import check_figures_equal, image_comparison
import pytest

def test_given_colors_levels_and_extends_5_mutated():
    plt.rcParams['pcolormesh.snap'] = False
    _, axs = plt.subplots(2, 4, sharex=True)
    data = np.arange(12).reshape(3, 4)
    colors = ['red', 'yellow', 'pink', 'blue', 'black']
    levels = [2, 4, 8, 10]
    for i, ax in enumerate(axs.flat):
        filled = i % 2 == 0.0
        extend = ['neither', 'min', 'max', 'both'][i // 2]
        if filled:
            first_color = 1 if extend in ['max', 'neither'] else None
            last_color = -1 if extend in ['min', 'neither'] else None
            c = ax.contourf(data, colors=colors[first_color:last_color], levels=levels, extend=extend)
        else:
            c = ax.contour(data, colors=colors[:-1], levels=levels, extend=extend)
        plt.colorbar(c, ax=ax)
# Mutation info: Added sharex = True (Call plt.subplots)