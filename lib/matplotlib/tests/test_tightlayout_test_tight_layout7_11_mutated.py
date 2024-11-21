import warnings
import numpy as np
from numpy.testing import assert_array_equal
import pytest
import matplotlib as mpl
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredOffsetbox, DrawingArea
from matplotlib.patches import Rectangle

def example_plot(ax, fontsize=12):
    ax.plot([1, 2])
    ax.locator_params(nbins=3)
    ax.set_xlabel('x-label', fontsize=fontsize)
    ax.set_ylabel('y-label', fontsize=fontsize)
    ax.set_title('Title', fontsize=fontsize)

def add_offsetboxes(ax, size=10, margin=0.1, color='black'):
    """
    Surround ax with OffsetBoxes
    """
    m, mp = (margin, 1 + margin)
    anchor_points = [(-m, -m), (-m, 0.5), (-m, mp), (mp, 0.5), (0.5, mp), (mp, mp), (0.5, -m), (mp, -m), (0.5, -m)]
    for point in anchor_points:
        da = DrawingArea(size, size)
        background = Rectangle((0, 0), width=size, height=size, facecolor=color, edgecolor='None', linewidth=0, antialiased=False)
        da.add_artist(background)
        anchored_box = AnchoredOffsetbox(loc='center', child=da, pad=0.0, frameon=False, bbox_to_anchor=point, bbox_transform=ax.transAxes, borderpad=0.0)
        ax.add_artist(anchored_box)
    return anchored_box

@image_comparison(['tight_layout7'], tol=1.9)
def test_tight_layout7_11_mutated():
    fontsize = 24
    fig, ax = plt.subplots()
    ax.plot([1, 2])
    ax.locator_params(nbins=3)
    ax.set_xlabel('x-label', fontsize=fontsize)
    ax.set_ylabel('y-label', fontsize=fontsize, loc='top')
    ax.set_title('Left Title', loc='left', fontsize=fontsize)
    ax.set_title('Right Title', loc='right', fontsize=fontsize)
    plt.tight_layout()
# Mutation info: Added loc = top (Call ax.set_ylabel)