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

@image_comparison(['contour_manual_labels'], remove_text=True, style='mpl20', tol=0.26)
def test_contour_manual_labels_1_mutated():
    x, y = np.meshgrid(np.arange(0, 10), np.arange(0, 10))
    z = np.max(np.dstack([abs(x), abs(y)]), 2)
    plt.figure(figsize=(6, 2), dpi=200, layout='none')
    cs = plt.contour(x, y, z)
    pts = np.array([(1.0, 3.0), (1.0, 4.4), (1.0, 6.0)])
    plt.clabel(cs, manual=pts)
    pts = np.array([(2.0, 3.0), (2.0, 4.4), (2.0, 6.0)])
    plt.clabel(cs, manual=pts, fontsize='small', colors=('r', 'g'))
# Mutation info: Added layout = none (Call plt.figure)