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

def test_wedge_range_13_mutated():
    ax = plt.axes(projection='hammer')
    t1 = 2.313869244286224
    args = [[52.31386924, 232.31386924], [52.313869244286224, 232.31386924428622], [t1, t1 + 180.0], [0, 360], [90, 90 + 360], [-180, 180], [0, 380], [45, 46], [46, 45]]
    for i, (theta1, theta2) in enumerate(args):
        x = i % 3
        y = i // 3
        wedge = mpatches.Wedge((x * 3, y * 3), 1, theta1, theta2, facecolor='none', edgecolor='k', lw=3)
        ax.add_artist(wedge)
    ax.set_xlim(-2, 8)
    ax.set_ylim(-2, 9)
# Mutation info: Added projection = hammer (Call plt.axes)