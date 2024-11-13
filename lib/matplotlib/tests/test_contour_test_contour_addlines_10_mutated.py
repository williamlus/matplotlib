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

def test_contour_addlines_10_mutated():
    plt.rcParams['pcolormesh.snap'] = False
    fig, ax = plt.subplots()
    np.random.seed(19680812)
    X = np.random.rand(10, 10) * 10000
    pcm = ax.pcolormesh(X, shading='nearest')
    cont = ax.contour(X + 1000)
    cb = fig.colorbar(pcm)
    cb.add_lines(cont)
    assert_array_almost_equal(cb.ax.get_ylim(), [114.3091, 9972.30735], 3)
# Mutation info: Added shading = nearest (Call ax.pcolormesh)