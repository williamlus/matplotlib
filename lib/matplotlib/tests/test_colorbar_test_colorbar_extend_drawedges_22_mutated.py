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

@image_comparison(['extend_drawedges.png'], remove_text=True, style='mpl20')
def test_colorbar_extend_drawedges_22_mutated():
    params = [('both', 1, [[[1.1, 0], [1.1, 1]], [[2, 0], [2, 1]], [[2.9, 0], [2.9, 1]]]), ('min', 0, [[[1.1, 0], [1.1, 1]], [[2, 0], [2, 1]]]), ('max', 0, [[[2, 0], [2, 1]], [[2.9, 0], [2.9, 1]]]), ('neither', -1, [[[2, 0], [2, 1]]])]
    plt.rcParams['axes.linewidth'] = 2
    fig = plt.figure(figsize=(10, 4), layout='constrained')
    subfigs = fig.subfigures(1, 2)
    for orientation, subfig in zip(['horizontal', 'vertical'], subfigs):
        if orientation == 'horizontal':
            axs = subfig.subplots(4, 1)
        else:
            axs = subfig.subplots(1, 4)
        fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
        for ax, (extend, coloroffset, res) in zip(axs, params):
            cmap = mpl.colormaps['viridis']
            bounds = np.arange(5)
            nb_colors = len(bounds) + coloroffset
            colors = cmap(np.linspace(100, 255, nb_colors).astype(int))
            cmap, norm = mcolors.from_levels_and_colors(bounds, colors, extend=extend)
            cbar = Colorbar(ax, cmap=cmap, norm=norm, orientation=orientation, drawedges=True)
            if orientation == 'horizontal':
                ax.set_xlim(1.1, 2.9)
            else:
                ax.set_ylim(1.1, 2.9)
                res = np.array(res)[:, :, [1, 0]]
            np.testing.assert_array_equal(cbar.dividers.get_segments(), res)
# Mutation info: Added layout = constrained (Call plt.figure)