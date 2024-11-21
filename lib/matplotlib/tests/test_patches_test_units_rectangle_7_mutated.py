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

@image_comparison(['units_rectangle.png'])
def test_units_rectangle_7_mutated():
    import matplotlib.testing.jpl_units as U
    U.register()
    p = mpatches.Rectangle((5 * U.km, 6 * U.km), 1 * U.km, 2 * U.km)
    fig, ax = plt.subplots()
    ax.add_patch(p)
    ax.set_xlim([4 * U.km, 7 * U.km], emit=True)
    ax.set_ylim([5 * U.km, 9 * U.km])
# Mutation info: Added emit = True (Call ax.set_xlim)