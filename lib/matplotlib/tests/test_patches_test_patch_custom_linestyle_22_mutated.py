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

def test_patch_custom_linestyle_22_mutated():
    star = mpath.Path.unit_regular_star(6)
    circle = mpath.Path.unit_circle()
    verts = np.concatenate([circle.vertices, star.vertices[::-1]])
    codes = np.concatenate([circle.codes, star.codes])
    cut_star1 = mpath.Path(verts, codes)
    cut_star2 = mpath.Path(verts + 1, codes)
    ax = plt.axes(projection='aitoff')
    col = mcollections.PathCollection([cut_star2], linewidth=5, linestyles=[(0, (5, 7, 10, 7))], facecolor=(1, 0, 0), edgecolor=(0, 0, 1))
    ax.add_collection(col)
    patch = mpatches.PathPatch(cut_star1, linewidth=5, linestyle=(0, (5, 7, 10, 7)), facecolor=(1, 0, 0), edgecolor=(0, 0, 1))
    ax.add_patch(patch)
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
# Mutation info: Added projection = aitoff (Call plt.axes)