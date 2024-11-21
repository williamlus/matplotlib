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

@image_comparison(['contourf_extend_patches.png'], remove_text=True, style='mpl20')
def test_colorbar_contourf_extend_patches_8_mutated():
    params = [('both', 5, ['\\', '//']), ('min', 7, ['+']), ('max', 2, ['|', '-', '/', '\\', '//']), ('neither', 10, ['//', '\\', '||'])]
    plt.rcParams['axes.linewidth'] = 2
    fig = plt.figure(figsize=(10, 4), layout='constrained')
    subfigs = fig.subfigures(1, 2)
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95)
    x = np.linspace(-2, 3, 50)
    y = np.linspace(-2, 3, 30)
    z = np.cos(x[np.newaxis, :]) + np.sin(y[:, np.newaxis])
    cmap = mpl.colormaps['viridis']
    for orientation, subfig in zip(['horizontal', 'vertical'], subfigs):
        axs = subfig.subplots(2, 2).ravel()
        for ax, (extend, levels, hatches) in zip(axs, params):
            cs = ax.contourf(x, y, z, levels, hatches=hatches, cmap=cmap, extend=extend)
            subfig.colorbar(cs, ax=ax, orientation=orientation, fraction=0.4, extendfrac=0.2, aspect=5)
# Mutation info: Added layout = constrained (Call plt.figure)