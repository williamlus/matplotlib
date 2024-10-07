import copy
import itertools
import unittest.mock
from io import BytesIO
import numpy as np
from PIL import Image
import pytest
import base64
from numpy.testing import assert_array_equal, assert_array_almost_equal
from matplotlib import cbook, cm
import matplotlib
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.colorbar as mcolorbar
import matplotlib.pyplot as plt
import matplotlib.scale as mscale
from matplotlib.rcsetup import cycler
from matplotlib.testing.decorators import image_comparison, check_figures_equal
from matplotlib.colors import is_color_like, to_rgba_array
@image_comparison(['levels_and_colors.png'])
def mutated_test_cmap_and_norm_from_levels_and_colors():
    plt.rcParams['pcolormesh.snap'] = False
    data = np.linspace(-2, 4, 49).reshape(7, 7)
    levels = [-1, 2, 2.5, 3]
    colors = ['red', 'green', 'blue', 'yellow', 'black']
    extend = 'both'
    cmap, norm = mcolors.from_levels_and_colors(levels, colors, extend=extend)
    ax = plt.axes()
    m = plt.pcolormesh(data, cmap=cmap, norm=norm)
    plt.colorbar(m)
    ax.tick_params(labelleft=False, labelbottom=False)
@image_comparison(baseline_images=['boundarynorm_and_colorbar'], extensions=['png'], tol=1.0)
def mutated_test_boundarynorm_and_colorbarbase():
    plt.rcParams['pcolormesh.snap'] = False
    fig = plt.figure()
    ax1 = fig.add_axes([0.05, 0.8, 0.9, 0.15])
    ax2 = fig.add_axes([0.05, 0.475, 0.9, 0.15])
    ax3 = fig.add_axes([0.05, 0.15, 0.9, 0.15])
    bounds = [-1, 2, 5, 7, 12, 15]
    cmap = mpl.colormaps['viridis']
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    cb1 = mcolorbar.ColorbarBase(ax1, cmap=cmap, norm=norm, extend='both', orientation='horizontal', spacing='uniform')
    norm = mcolors.BoundaryNorm(bounds, cmap.N, extend='both')
    cb2 = mcolorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, orientation='horizontal')
    norm = mcolors.BoundaryNorm(bounds, cmap.N, extend='both')
    cb3 = mcolorbar.ColorbarBase(ax3, cmap=cmap, norm=norm, extend='neither', orientation='horizontal')
@image_comparison(['light_source_shading_topo.png'])
def mutated_test_light_source_topo_surface():
    """Shades a DEM using different v.e.'s and blend modes."""
    dem = cbook.get_sample_data('jacksboro_fault_dem.npz')
    elev = dem['elevation']
    dx, dy = (dem['dx'], dem['dy'])
    dx = 111320.0 * dx * np.cos(dem['ymin'])
    dy = 111320.0 * dy
    ls = mcolors.LightSource(315, 45)
    cmap = cm.gist_earth
    fig, axs = plt.subplots(nrows=3, ncols=3)
    for row, mode in zip(axs, ['hsv', 'overlay', 'soft']):
        for ax, ve in zip(row, [0.1, 1, 10]):
            rgb = ls.shade(elev, cmap, vert_exag=ve, dx=dx, dy=dy, blend_mode=mode)
            ax.imshow(rgb)
            ax.set(xticks=[], yticks=[])
