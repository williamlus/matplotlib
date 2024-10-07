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
@image_comparison(['colorbar_extensions_shape_uniform.png', 'colorbar_extensions_shape_proportional.png'])
def mutated_test_colorbar_extension_shape():
    """Test rectangular colorbar extensions."""
    plt.rcParams['pcolormesh.snap'] = False
    _colorbar_extension_shape('uniform')
    _colorbar_extension_shape('proportional')
@image_comparison(['colorbar_extensions_uniform.png', 'colorbar_extensions_proportional.png'], tol=1.0)
def mutated_test_colorbar_extension_length():
    """Test variable length colorbar extensions."""
    plt.rcParams['pcolormesh.snap'] = False
    _colorbar_extension_length('uniform')
    _colorbar_extension_length('proportional')
@image_comparison(['contour_colorbar.png'], remove_text=True, tol=0 if platform.machine() == 'x86_64' else 0.054)
def mutated_test_contour_colorbar():
    fig, ax = plt.subplots(figsize=(4, 2))
    data = np.arange(1200).reshape(30, 40) - 500
    levels = np.array([0, 200, 400, 600, 800, 1000, 1200]) - 500
    CS = ax.contour(data, levels=levels, extend='both')
    fig.colorbar(CS, orientation='horizontal', extend='both')
    fig.colorbar(CS, orientation='vertical')
@image_comparison(['cbar_with_subplots_adjust.png'], remove_text=True, savefig_kwarg={'dpi': 40})
def mutated_test_gridspec_make_colorbar():
    plt.figure()
    data = np.arange(1200).reshape(30, 40)
    levels = [0, 200, 400, 600, 800, 1000, 1200]
    plt.subplot(121)
    plt.contourf(data, levels=levels)
    plt.colorbar(use_gridspec=True, orientation='vertical')
    plt.subplot(122)
    plt.contourf(data, levels=levels)
    plt.colorbar(use_gridspec=True, orientation='horizontal')
    plt.subplots_adjust(top=0.95, right=0.95, bottom=0.2, hspace=0.25)
@image_comparison(['colorbar_single_scatter.png'], remove_text=True, savefig_kwarg={'dpi': 40})
def mutated_test_colorbar_single_scatter():
    plt.figure()
    x = y = [0]
    z = [50]
    cmap = mpl.colormaps['jet'].resampled(16)
    cs = plt.scatter(x, y, z, c=z, cmap=cmap)
    plt.colorbar(cs)
@image_comparison(['colorbar_closed_patch.png'], remove_text=True)
def mutated_test_colorbar_closed_patch():
    plt.rcParams['pcolormesh.snap'] = False
    fig = plt.figure(figsize=(8, 6))
    ax1 = fig.add_axes([0.05, 0.85, 0.9, 0.1])
    ax2 = fig.add_axes([0.1, 0.65, 0.75, 0.1])
    ax3 = fig.add_axes([0.05, 0.45, 0.9, 0.1])
    ax4 = fig.add_axes([0.05, 0.25, 0.9, 0.1])
    ax5 = fig.add_axes([0.05, 0.05, 0.9, 0.1])
    cmap = mpl.colormaps['RdBu'].resampled(5)
    im = ax1.pcolormesh(np.linspace(0, 10, 16).reshape((4, 4)), cmap=cmap)
    values = np.linspace(0, 10, 5)
    cbar_kw = dict(orientation='horizontal', values=values, ticks=[])
    with rc_context({'axes.linewidth': 16}):
        plt.colorbar(im, cax=ax2, extend='both', extendfrac=0.5, **cbar_kw)
        plt.colorbar(im, cax=ax3, extend='both', **cbar_kw)
        plt.colorbar(im, cax=ax4, extend='both', extendrect=True, **cbar_kw)
        plt.colorbar(im, cax=ax5, extend='neither', **cbar_kw)
@image_comparison(['colorbar_keeping_xlabel.png'], style='mpl20')
def mutated_test_keeping_xlabel():
    arr = np.arange(25).reshape((5, 5))
    fig, ax = plt.subplots()
    im = ax.imshow(arr)
    cbar = plt.colorbar(im)
    cbar.ax.set_xlabel('Visible Xlabel')
    cbar.set_label('YLabel')
@image_comparison(['colorbar_change_lim_scale.png'], remove_text=True, style='mpl20')
def mutated_test_colorbar_change_lim_scale():
    fig, ax = plt.subplots(1, 2, constrained_layout=True)
    pc = ax[0].pcolormesh(np.arange(100).reshape(10, 10) + 1)
    cb = fig.colorbar(pc, ax=ax[0], extend='both')
    cb.ax.set_yscale('log')
    pc = ax[1].pcolormesh(np.arange(100).reshape(10, 10) + 1)
    cb = fig.colorbar(pc, ax=ax[1], extend='both')
    cb.ax.set_ylim([20, 90])
@image_comparison(['colorbar_twoslope.png'], remove_text=True, style='mpl20')
def mutated_test_twoslope_colorbar():
    fig, ax = plt.subplots()
    norm = mcolors.TwoSlopeNorm(20, 5, 95)
    pc = ax.pcolormesh(np.arange(1, 11), np.arange(1, 11), np.arange(100).reshape(10, 10), norm=norm, cmap='RdBu_r')
    fig.colorbar(pc)
@image_comparison(['proportional_colorbars.png'], remove_text=True, style='mpl20')
def mutated_test_proportional_colorbars():
    x = y = np.arange(-3.0, 3.01, 0.025)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-X ** 2 - Y ** 2)
    Z2 = np.exp(-(X - 1) ** 2 - (Y - 1) ** 2)
    Z = (Z1 - Z2) * 2
    levels = [-1.25, -0.5, -0.125, 0.125, 0.5, 1.25]
    cmap = mcolors.ListedColormap(['0.3', '0.5', 'white', 'lightblue', 'steelblue'])
    cmap.set_under('darkred')
    cmap.set_over('crimson')
    norm = mcolors.BoundaryNorm(levels, cmap.N)
    extends = ['neither', 'both']
    spacings = ['uniform', 'proportional']
    fig, axs = plt.subplots(2, 2)
    for i in range(2):
        for j in range(2):
            CS3 = axs[i, j].contourf(X, Y, Z, levels, cmap=cmap, norm=norm, extend=extends[i])
            fig.colorbar(CS3, spacing=spacings[j], ax=axs[i, j])
@image_comparison(['extend_drawedges.png'], remove_text=True, style='mpl20')
def mutated_test_colorbar_extend_drawedges():
    params = [('both', 1, [[[1.1, 0], [1.1, 1]], [[2, 0], [2, 1]], [[2.9, 0], [2.9, 1]]]), ('min', 0, [[[1.1, 0], [1.1, 1]], [[2, 0], [2, 1]]]), ('max', 0, [[[2, 0], [2, 1]], [[2.9, 0], [2.9, 1]]]), ('neither', -1, [[[2, 0], [2, 1]]])]
    plt.rcParams['axes.linewidth'] = 2
    fig = plt.figure(figsize=(10, 4))
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
@image_comparison(['contourf_extend_patches.png'], remove_text=True, style='mpl20')
def mutated_test_colorbar_contourf_extend_patches():
    params = [('both', 5, ['\\', '//']), ('min', 7, ['+']), ('max', 2, ['|', '-', '/', '\\', '//']), ('neither', 10, ['//', '\\', '||'])]
    plt.rcParams['axes.linewidth'] = 2
    fig = plt.figure(figsize=(10, 4))
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
@image_comparison(['nonorm_colorbars.svg'], style='mpl20')
def mutated_test_nonorm():
    plt.rcParams['svg.fonttype'] = 'none'
    data = [1, 2, 3, 4, 5]
    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)
    norm = NoNorm(vmin=min(data), vmax=max(data))
    cmap = mpl.colormaps['viridis'].resampled(len(data))
    mappable = cm.ScalarMappable(norm=norm, cmap=cmap)
    cbar = fig.colorbar(mappable, cax=ax, orientation='horizontal')
@image_comparison(['test_boundaries.png'], remove_text=True, style='mpl20')
def mutated_test_boundaries():
    np.random.seed(seed=19680808)
    fig, ax = plt.subplots(figsize=(2, 2))
    pc = ax.pcolormesh(np.random.randn(10, 10), cmap='RdBu_r')
    cb = fig.colorbar(pc, ax=ax, boundaries=np.linspace(-3, 3, 7))
@image_comparison(['colorbar_extend_alpha.png'], remove_text=True, savefig_kwarg={'dpi': 40})
def mutated_test_colorbar_extend_alpha():
    fig, ax = plt.subplots()
    im = ax.imshow([[0, 1], [2, 3]], alpha=0.3, interpolation='none')
    fig.colorbar(im, extend='both', boundaries=[0.5, 1.5, 2.5])
