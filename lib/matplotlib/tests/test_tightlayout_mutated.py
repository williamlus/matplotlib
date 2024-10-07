import warnings
import numpy as np
from numpy.testing import assert_array_equal
import pytest
import matplotlib as mpl
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredOffsetbox, DrawingArea
from matplotlib.patches import Rectangle
@image_comparison(['tight_layout1'], tol=1.9)
def mutated_test_tight_layout1():
    """Test tight_layout for a single subplot."""
    fig, ax = plt.subplots()
    example_plot(ax, fontsize=24)
    plt.tight_layout()
@image_comparison(['tight_layout2'])
def mutated_test_tight_layout2():
    """Test tight_layout for multiple subplots."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
    example_plot(ax1)
    example_plot(ax2)
    example_plot(ax3)
    example_plot(ax4)
    plt.tight_layout()
@image_comparison(['tight_layout3'])
def mutated_test_tight_layout3():
    """Test tight_layout for multiple subplots."""
    ax1 = plt.subplot(221)
    ax2 = plt.subplot(223)
    ax3 = plt.subplot(122)
    example_plot(ax1)
    example_plot(ax2)
    example_plot(ax3)
    plt.tight_layout()
@image_comparison(['tight_layout4'], freetype_version=('2.5.5', '2.6.1'), tol=0.015)
def mutated_test_tight_layout4():
    """Test tight_layout for subplot2grid."""
    ax1 = plt.subplot2grid((3, 3), (0, 0))
    ax2 = plt.subplot2grid((3, 3), (0, 1), colspan=2)
    ax3 = plt.subplot2grid((3, 3), (1, 0), colspan=2, rowspan=2)
    ax4 = plt.subplot2grid((3, 3), (1, 2), rowspan=2)
    example_plot(ax1)
    example_plot(ax2)
    example_plot(ax3)
    example_plot(ax4)
    plt.tight_layout()
@image_comparison(['tight_layout5'])
def mutated_test_tight_layout5():
    """Test tight_layout for image."""
    ax = plt.subplot()
    arr = np.arange(100).reshape((10, 10))
    ax.imshow(arr, interpolation='none')
    plt.tight_layout()
@image_comparison(['tight_layout6'])
def mutated_test_tight_layout6():
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
        ax.set_xlabel('x-label', fontsize=12)
        gs2.tight_layout(fig, rect=[0.5, 0, 1, 1], h_pad=0.45)
        top = min(gs1.top, gs2.top)
        bottom = max(gs1.bottom, gs2.bottom)
        gs1.tight_layout(fig, rect=[None, 0 + (bottom - gs1.bottom), 0.5, 1 - (gs1.top - top)])
        gs2.tight_layout(fig, rect=[0.5, 0 + (bottom - gs2.bottom), None, 1 - (gs2.top - top)], h_pad=0.45)
@image_comparison(['tight_layout7'], tol=1.9)
def mutated_test_tight_layout7():
    fontsize = 24
    fig, ax = plt.subplots()
    ax.plot([1, 2])
    ax.locator_params(nbins=3)
    ax.set_xlabel('x-label', fontsize=fontsize)
    ax.set_ylabel('y-label', fontsize=fontsize)
    ax.set_title('Left Title', loc='left', fontsize=fontsize)
    ax.set_title('Right Title', loc='right', fontsize=fontsize)
    plt.tight_layout()
@image_comparison(['tight_layout8'], tol=0.005)
def mutated_test_tight_layout8():
    """Test automatic use of tight_layout."""
    fig = plt.figure()
    fig.set_layout_engine(layout='tight', pad=0.1)
    ax = fig.add_subplot()
    example_plot(ax, fontsize=24)
    fig.draw_without_rendering()
@image_comparison(['tight_layout9'])
def mutated_test_tight_layout9():
    f, axarr = plt.subplots(2, 2)
    axarr[1][1].set_visible(False)
    plt.tight_layout()
@image_comparison(['tight_layout_offsetboxes1', 'tight_layout_offsetboxes2'])
def mutated_test_tight_layout_offsetboxes():
    rows = cols = 2
    colors = ['red', 'blue', 'green', 'yellow']
    x = y = [0, 1]

    def _subplots():
        _, axs = plt.subplots(rows, cols)
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
