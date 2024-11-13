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

def test_line_dashes_2_mutated():
    fig, ax = plt.subplots(sharey=True)
    ax.plot(range(10), linestyle=(0, (3, 3)), lw=5)
# Mutation info: Added sharey = True (Call plt.subplots)