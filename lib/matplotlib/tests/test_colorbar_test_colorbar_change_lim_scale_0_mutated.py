import platform
import numpy as np
import pytest
from matplotlib import cm
import matplotlib.colors as mcolors
import matplotlib as mpl
from matplotlib import rc_context
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, LogNorm, PowerNorm, Normalize, NoNorm
from matplotlib.colorbar import Colorbar
from matplotlib.ticker import FixedLocator, LogFormatter, StrMethodFormatter
from matplotlib.testing.decorators import check_figures_equal

def _get_cmap_norms():
    """
    Define a colormap and appropriate norms for each of the four
    possible settings of the extend keyword.

    Helper function for _colorbar_extension_shape and
    colorbar_extension_length.
    """
    cmap = mpl.colormaps['RdBu'].resampled(5)
    clevs = [-5.0, -2.5, -0.5, 0.5, 1.5, 3.5]
    norms = dict()
    norms['neither'] = BoundaryNorm(clevs, len(clevs) - 1)
    norms['min'] = BoundaryNorm([-10] + clevs[1:], len(clevs) - 1)
    norms['max'] = BoundaryNorm(clevs[:-1] + [10], len(clevs) - 1)
    norms['both'] = BoundaryNorm([-10] + clevs[1:-1] + [10], len(clevs) - 1)
    return (cmap, norms)

def _colorbar_extension_shape(spacing):
    """
    Produce 4 colorbars with rectangular extensions for either uniform
    or proportional spacing.

    Helper function for test_colorbar_extension_shape.
    """
    cmap, norms = _get_cmap_norms()
    fig = plt.figure()
    fig.subplots_adjust(hspace=4)
    for i, extension_type in enumerate(('neither', 'min', 'max', 'both')):
        norm = norms[extension_type]
        boundaries = values = norm.boundaries
        values = values[:-1]
        cax = fig.add_subplot(4, 1, i + 1)
        Colorbar(cax, cmap=cmap, norm=norm, boundaries=boundaries, values=values, extend=extension_type, extendrect=True, orientation='horizontal', spacing=spacing)
        cax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    return fig

def _colorbar_extension_length(spacing):
    """
    Produce 12 colorbars with variable length extensions for either
    uniform or proportional spacing.

    Helper function for test_colorbar_extension_length.
    """
    cmap, norms = _get_cmap_norms()
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.6)
    for i, extension_type in enumerate(('neither', 'min', 'max', 'both')):
        norm = norms[extension_type]
        boundaries = values = norm.boundaries
        values = values[:-1]
        for j, extendfrac in enumerate((None, 'auto', 0.1)):
            cax = fig.add_subplot(12, 1, i * 3 + j + 1)
            Colorbar(cax, cmap=cmap, norm=norm, boundaries=boundaries, values=values, extend=extension_type, extendfrac=extendfrac, orientation='horizontal', spacing=spacing)
            cax.tick_params(left=False, labelleft=False, bottom=False, labelbottom=False)
    return fig

@image_comparison(['colorbar_change_lim_scale.png'], remove_text=True, style='mpl20')
def test_colorbar_change_lim_scale_0_mutated():
    fig, ax = plt.subplots(1, 2, constrained_layout=True, sharex=True)
    pc = ax[0].pcolormesh(np.arange(100).reshape(10, 10) + 1)
    cb = fig.colorbar(pc, ax=ax[0], extend='both')
    cb.ax.set_yscale('log')
    pc = ax[1].pcolormesh(np.arange(100).reshape(10, 10) + 1)
    cb = fig.colorbar(pc, ax=ax[1], extend='both')
    cb.ax.set_ylim([20, 90])
# Mutation info: Added sharex = True (Call plt.subplots)