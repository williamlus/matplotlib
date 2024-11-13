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

def test_lw_scaling_3_mutated():
    th = np.linspace(0, 32)
    fig, ax = plt.subplots(sharex=True)
    lins_styles = ['dashed', 'dotted', 'dashdot']
    cy = cycler(matplotlib.rcParams['axes.prop_cycle'])
    for j, (ls, sty) in enumerate(zip(lins_styles, cy)):
        for lw in np.linspace(0.5, 10, 10):
            ax.plot(th, j * np.ones(50) + 0.1 * lw, linestyle=ls, lw=lw, **sty)
# Mutation info: Added sharex = True (Call plt.subplots)