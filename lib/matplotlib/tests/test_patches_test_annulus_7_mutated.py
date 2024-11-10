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

def test_annulus_7_mutated():
    fig, ax = plt.subplots()
    cir = Annulus((0.5, 0.5), 0.2, 0.05, fc='g')
    ell = Annulus((0.5, 0.5), (0.5, 0.3), 0.1, 45, fc='m', ec='b', alpha=0.5, hatch='xxx')
    ax.add_patch(cir)
    ax.add_patch(ell)
    ax.set_aspect('equal', share=True)