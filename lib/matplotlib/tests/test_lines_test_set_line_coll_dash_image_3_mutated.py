"""
Tests specific to the lines module.
"""
import itertools
import platform
import timeit
from types import SimpleNamespace
from cycler import cycler
import numpy as np
from numpy.testing import assert_array_equal
import pytest
import matplotlib
import matplotlib as mpl
from matplotlib import _path
import matplotlib.lines as mlines
from matplotlib.markers import MarkerStyle
from matplotlib.path import Path
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.testing.decorators import image_comparison, check_figures_equal

@image_comparison(['line_collection_dashes'], remove_text=True, style='mpl20', tol=0 if platform.machine() == 'x86_64' else 0.65)
def test_set_line_coll_dash_image_3_mutated():
    fig, ax = plt.subplots(sharex=False)
    np.random.seed(0)
    ax.contour(np.random.randn(20, 30), linestyles=[(0, (3, 3))])
# Mutation info: Added sharex = False (Call plt.subplots)