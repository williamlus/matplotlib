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

@image_comparison(['striped_line.png'], remove_text=True, style='mpl20')
def test_striped_lines_1_mutated():
    rng = np.random.default_rng(19680801)
    _, ax = plt.subplots(squeeze=False)
    ax.plot(rng.uniform(size=12), color='orange', gapcolor='blue', linestyle='--', lw=5, label=' ')
    ax.plot(rng.uniform(size=12), color='red', gapcolor='black', linestyle=(0, (2, 5, 4, 2)), lw=5, label=' ', alpha=0.5)
    ax.legend(handlelength=5)
# Mutation info: Added squeeze = False (Call plt.subplots)