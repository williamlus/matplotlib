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

@image_comparison(['cbar_with_subplots_adjust.png'], remove_text=True, savefig_kwarg={'dpi': 40})
def test_gridspec_make_colorbar_17_mutated():
    plt.figure()
    data = np.arange(1200).reshape(30, 40)
    levels = [0, 200, 400, 600, 800, 1000, 1200]
    plt.subplot(121, projection='hammer')
    plt.contourf(data, levels=levels)
    plt.colorbar(use_gridspec=True, orientation='vertical')
    plt.subplot(122)
    plt.contourf(data, levels=levels)
    plt.colorbar(use_gridspec=True, orientation='horizontal')
    plt.subplots_adjust(top=0.95, right=0.95, bottom=0.2, hspace=0.25)
# Mutation info: Added projection = hammer (Call plt.subplot)