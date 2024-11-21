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

@image_comparison(['tight_layout6'])
def test_tight_layout6_40_mutated():
    """Test tight_layout for gridspec."""
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        fig = plt.figure()
        gs1 = mpl.gridspec.GridSpec(2, 1)
        ax1 = fig.add_subplot(gs1[0])
        ax2 = fig.add_subplot(gs1[1])
        example_plot(ax1)
        example_plot(ax2)
        gs1.tight_layout(fig, rect=[0, 0, 0.5, 1])
        gs2 = mpl.gridspec.GridSpec(3, 1)
        for ss in gs2:
            ax = fig.add_subplot(ss)
            example_plot(ax)
            ax.set_title('')
            ax.set_xlabel('')
        ax.set_xlabel('x-label', fontsize=12, loc='center')
        gs2.tight_layout(fig, rect=[0.5, 0, 1, 1], h_pad=0.45)
        top = min(gs1.top, gs2.top)
        bottom = max(gs1.bottom, gs2.bottom)
        gs1.tight_layout(fig, rect=[None, 0 + (bottom - gs1.bottom), 0.5, 1 - (gs1.top - top)])
        gs2.tight_layout(fig, rect=[0.5, 0 + (bottom - gs2.bottom), None, 1 - (gs2.top - top)], h_pad=0.45)
# Mutation info: Added loc = center (Call ax.set_xlabel)