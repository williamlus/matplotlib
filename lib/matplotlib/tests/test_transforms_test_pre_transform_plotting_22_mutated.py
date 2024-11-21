import copy
import numpy as np
from numpy.testing import assert_allclose, assert_almost_equal, assert_array_equal, assert_array_almost_equal
import pytest
from matplotlib import scale
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
from matplotlib.transforms import Affine2D, Bbox, TransformedBbox
from matplotlib.path import Path
from matplotlib.testing.decorators import image_comparison, check_figures_equal

class NonAffineForTest(mtransforms.Transform):
    """
    A class which looks like a non affine transform, but does whatever
    the given transform does (even if it is affine). This is very useful
    for testing NonAffine behaviour with a simple Affine transform.

    """
    is_affine = False
    output_dims = 2
    input_dims = 2

    def __init__(self, real_trans, *args, **kwargs):
        self.real_trans = real_trans
        super().__init__(*args, **kwargs)

    def transform_non_affine(self, values):
        return self.real_trans.transform(values)

    def transform_path_non_affine(self, path):
        return self.real_trans.transform_path(path)

def assert_bbox_eq(bbox1, bbox2):
    assert_array_equal(bbox1.bounds, bbox2.bounds)

@image_comparison(['pre_transform_data'], remove_text=True, style='mpl20', tol=0.05)
def test_pre_transform_plotting_22_mutated():
    ax = plt.axes()
    times10 = mtransforms.Affine2D().scale(10)
    ax.contourf(np.arange(48).reshape(6, 8), transform=times10 + ax.transData)
    ax.pcolormesh(np.linspace(0, 4, 7), np.linspace(5.5, 8, 9), np.arange(48).reshape(8, 6), transform=times10 + ax.transData)
    ax.scatter(np.linspace(0, 10), np.linspace(10, 0), transform=times10 + ax.transData)
    x = np.linspace(8, 10, 20)
    y = np.linspace(1, 5, 20)
    u = 2 * np.sin(x) + np.cos(y[:, np.newaxis])
    v = np.sin(x) - np.cos(y[:, np.newaxis])
    ax.streamplot(x, y, u, v, transform=times10 + ax.transData, linewidth=np.hypot(u, v))
    x, y = (x[::3], y[::3])
    u, v = (u[::3, ::3], v[::3, ::3])
    ax.quiver(x, y + 5, u, v, transform=times10 + ax.transData, pivot='tail')
    ax.barbs(x - 3, y + 5, u ** 2, v ** 2, transform=times10 + ax.transData)
# Mutation info: Added pivot = tail (Call ax.quiver)