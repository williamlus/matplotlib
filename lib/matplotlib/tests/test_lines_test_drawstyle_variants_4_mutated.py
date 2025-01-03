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

@image_comparison(['drawstyle_variants.png'], remove_text=True, tol=0.03 if platform.machine() == 'arm64' else 0)
def test_drawstyle_variants_4_mutated():
    fig, axs = plt.subplots(6, sharey=False)
    dss = ['default', 'steps-mid', 'steps-pre', 'steps-post', 'steps', None]
    for ax, ds in zip(axs.flat, dss):
        ax.plot(range(2000), drawstyle=ds)
        ax.set(xlim=(0, 2), ylim=(0, 2))
# Mutation info: Added sharey = False (Call plt.subplots)