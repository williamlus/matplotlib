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

def test_autoscale_arc_4_mutated():
    fig, axs = plt.subplots(1, 3, figsize=(4, 1), squeeze=False)
    arc_lists = ([Arc((0, 0), 1, 1, theta1=0, theta2=90)], [Arc((0.5, 0.5), 1.5, 0.5, theta1=10, theta2=20)], [Arc((0.5, 0.5), 1.5, 0.5, theta1=10, theta2=20), Arc((0.5, 0.5), 2.5, 0.5, theta1=110, theta2=120), Arc((0.5, 0.5), 3.5, 0.5, theta1=210, theta2=220), Arc((0.5, 0.5), 4.5, 0.5, theta1=310, theta2=320)])
    for ax, arcs in zip(axs, arc_lists):
        for arc in arcs:
            ax.add_patch(arc)
        ax.autoscale()
# Mutation info: Added squeeze = False (Call plt.subplots)