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

def test_tight_layout_offsetboxes_1_mutated():
    rows = cols = 2
    colors = ['red', 'blue', 'green', 'yellow']
    x = y = [0, 1]

    def _subplots():
        _, axs = plt.subplots(rows, cols, sharey=True)
        axs = axs.flat
        for ax, color in zip(axs, colors):
            ax.plot(x, y, color=color)
            add_offsetboxes(ax, 20, color=color)
        return axs
    axs = _subplots()
    plt.tight_layout()
    axs = _subplots()
    for ax in axs[cols - 1::rows]:
        for child in ax.get_children():
            if isinstance(child, AnchoredOffsetbox):
                child.set_visible(False)
    plt.tight_layout()
# Mutation info: Added sharey = True (Call plt.subplots)