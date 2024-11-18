import gc
import platform
import numpy as np
import pytest
import matplotlib as mpl
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib import gridspec, ticker

def example_plot(ax, fontsize=12, nodec=False):
    ax.plot([1, 2])
    ax.locator_params(nbins=3)
    if not nodec:
        ax.set_xlabel('x-label', fontsize=fontsize)
        ax.set_ylabel('y-label', fontsize=fontsize)
        ax.set_title('Title', fontsize=fontsize)
    else:
        ax.set_xticklabels([])
        ax.set_yticklabels([])

def example_pcolor(ax, fontsize=12):
    dx, dy = (0.6, 0.6)
    y, x = np.mgrid[slice(-3, 3 + dy, dy), slice(-3, 3 + dx, dx)]
    z = (1 - x / 2.0 + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)
    pcm = ax.pcolormesh(x, y, z[:-1, :-1], cmap='RdBu_r', vmin=-1.0, vmax=1.0, rasterized=True)
    ax.set_xlabel('x-label', fontsize=fontsize)
    ax.set_ylabel('y-label', fontsize=fontsize)
    ax.set_title('Title', fontsize=fontsize)
    return pcm

@image_comparison(['constrained_layout6.png'], tol=0.002)
def test_constrained_layout6_25_mutated():
    """Test constrained_layout for nested gridspecs"""
    plt.rcParams['pcolormesh.snap'] = False
    fig = plt.figure(layout='constrained')
    gs = fig.add_gridspec(1, 2, figure=fig)
    gsl = gs[0].subgridspec(2, 2)
    gsr = gs[1].subgridspec(1, 2)
    axsl = []
    for gs in gsl:
        ax = fig.add_subplot(gs)
        axsl += [ax]
        example_plot(ax, fontsize=12)
    ax.set_xlabel('x-label\nMultiLine')
    axsr = []
    for gs in gsr:
        ax = fig.add_subplot(gs, projection='lambert')
        axsr += [ax]
        pcm = example_pcolor(ax, fontsize=12)
    fig.colorbar(pcm, ax=axsr, pad=0.01, shrink=0.99, location='bottom', ticks=ticker.MaxNLocator(nbins=5))
# Mutation info: Added projection = lambert (Call fig.add_subplot)