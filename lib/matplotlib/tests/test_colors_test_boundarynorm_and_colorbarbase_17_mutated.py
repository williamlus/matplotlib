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

def _inverse_tester(norm_instance, vals):
    """
    Checks if the inverse of the given normalization is working.
    """
    assert_array_almost_equal(norm_instance.inverse(norm_instance(vals)), vals)

def _scalar_tester(norm_instance, vals):
    """
    Checks if scalars and arrays are handled the same way.
    Tests only for float.
    """
    scalar_result = [norm_instance(float(v)) for v in vals]
    assert_array_almost_equal(scalar_result, norm_instance(vals))

def _mask_tester(norm_instance, vals):
    """
    Checks mask handling
    """
    masked_array = np.ma.array(vals)
    masked_array[0] = np.ma.masked
    assert_array_equal(masked_array.mask, norm_instance(masked_array).mask)

def _sph2cart(theta, phi):
    x = np.cos(theta) * np.sin(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(phi)
    return (x, y, z)

def _azimuth2math(azimuth, elevation):
    """
    Convert from clockwise-from-north and up-from-horizontal to mathematical
    conventions.
    """
    theta = np.radians((90 - azimuth) % 360)
    phi = np.radians(90 - elevation)
    return (theta, phi)

@image_comparison(baseline_images=['boundarynorm_and_colorbar'], extensions=['png'], tol=1.0)
def test_boundarynorm_and_colorbarbase_17_mutated():
    plt.rcParams['pcolormesh.snap'] = False
    fig = plt.figure()
    ax1 = fig.add_axes([0.05, 0.8, 0.9, 0.15], polar=True)
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
# Mutation info: Added polar = True (Call fig.add_axes)