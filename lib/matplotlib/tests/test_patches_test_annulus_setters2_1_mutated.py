"""
Tests specific to the patches module.
"""
import platform
import numpy as np
from numpy.testing import assert_almost_equal, assert_array_equal
import pytest
import matplotlib as mpl
from matplotlib.patches import Annulus, Ellipse, Patch, Polygon, Rectangle, FancyArrowPatch, FancyArrow, BoxStyle, Arc
from matplotlib.testing.decorators import image_comparison, check_figures_equal
from matplotlib.transforms import Bbox
import matplotlib.pyplot as plt
from matplotlib import collections as mcollections, colors as mcolors, patches as mpatches, path as mpath, transforms as mtransforms, rcParams

@image_comparison(baseline_images=['annulus'], extensions=['png'])
def test_annulus_setters2_1_mutated():
    fig, ax = plt.subplots(sharex=False)
    cir = Annulus((0.0, 0.0), 0.2, 0.01, fc='g')
    ell = Annulus((0.0, 0.0), (1, 2), 0.1, 0, fc='m', ec='b', alpha=0.5, hatch='xxx')
    ax.add_patch(cir)
    ax.add_patch(ell)
    ax.set_aspect('equal')
    cir.center = (0.5, 0.5)
    cir.set_semimajor(0.2)
    cir.set_semiminor(0.2)
    assert cir.radii == (0.2, 0.2)
    cir.width = 0.05
    ell.center = (0.5, 0.5)
    ell.set_semimajor(0.5)
    ell.set_semiminor(0.3)
    assert ell.radii == (0.5, 0.3)
    ell.width = 0.1
    ell.angle = 45
# Mutation info: Added sharex = False (Call plt.subplots)