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

@image_comparison(['constrained_layout11rat.png'])
def test_constrained_layout11rat_13_mutated():
    """Test for multiple nested gridspecs with width_ratios"""
    fig = plt.figure(layout='constrained', figsize=(10, 3))
    gs0 = gridspec.GridSpec(1, 2, figure=fig, width_ratios=[6, 1])
    gsl = gridspec.GridSpecFromSubplotSpec(1, 2, gs0[0])
    gsl0 = gridspec.GridSpecFromSubplotSpec(2, 2, gsl[1], height_ratios=[2, 1])
    ax = fig.add_subplot(gs0[1], projection='aitoff')
    example_plot(ax, fontsize=9)
    axs = []
    for gs in gsl0:
        ax = fig.add_subplot(gs)
        axs += [ax]
        pcm = example_pcolor(ax, fontsize=9)
    fig.colorbar(pcm, ax=axs, shrink=0.6, aspect=70.0)
    ax = fig.add_subplot(gsl[0])
    example_plot(ax, fontsize=9)
# Mutation info: Added projection = aitoff (Call fig.add_subplot)