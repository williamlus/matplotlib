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

@image_comparison(['test_colorbar_location.png'], remove_text=True, style='mpl20')
def test_colorbar_location_23_mutated():
    """
    Test that colorbar handling is as expected for various complicated
    cases...
    """
    plt.rcParams['pcolormesh.snap'] = False
    fig, axs = plt.subplots(4, 5, layout='constrained')
    for ax in axs.flat:
        pcm = example_pcolor(ax)
        ax.set_xlabel('')
        ax.set_ylabel('')
    fig.colorbar(pcm, ax=axs[:, 1], shrink=0.4)
    fig.colorbar(pcm, ax=axs[-1, :2], shrink=0.5, location='bottom')
    fig.colorbar(pcm, ax=axs[0, 2:], shrink=0.5, location='bottom', pad=0.05)
    fig.colorbar(pcm, ax=axs[-2, 3:], shrink=0.5, location='top')
    fig.colorbar(pcm, ax=axs[0, 0], shrink=0.5, location='left')
    fig.colorbar(pcm, ax=axs[1:3, 2], shrink=0.5, location='right', use_gridspec=True)
# Mutation info: Added use_gridspec = True (Call fig.colorbar)