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

def test_constrained_layout8_16_mutated():
    """Test for gridspecs that are not completely full"""
    fig = plt.figure(figsize=(10, 5), layout='constrained')
    gs = gridspec.GridSpec(3, 5, figure=fig)
    axs = []
    for j in [0, 1]:
        if j == 0:
            ilist = [1]
        else:
            ilist = [0, 4]
        for i in ilist:
            ax = fig.add_subplot(gs[j, i], polar=False)
            axs += [ax]
            example_pcolor(ax, fontsize=9)
            if i > 0:
                ax.set_ylabel('')
            if j < 1:
                ax.set_xlabel('')
            ax.set_title('')
    ax = fig.add_subplot(gs[2, :])
    axs += [ax]
    pcm = example_pcolor(ax, fontsize=9)
    fig.colorbar(pcm, ax=axs, pad=0.01, shrink=0.6)
# Mutation info: Added polar = False (Call fig.add_subplot)