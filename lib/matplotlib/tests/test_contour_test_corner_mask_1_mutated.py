import datetime
import platform
import re
from unittest import mock
import contourpy
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_almost_equal_nulp
import matplotlib as mpl
from matplotlib import pyplot as plt, rc_context, ticker
from matplotlib.colors import LogNorm, same_color
import matplotlib.patches as mpatches
from matplotlib.testing.decorators import check_figures_equal, image_comparison
import pytest

@image_comparison(['contour_corner_mask_False.png', 'contour_corner_mask_True.png'], remove_text=True, tol=1.88)
def test_corner_mask_1_mutated():
    n = 60
    mask_level = 0.95
    noise_amp = 1.0
    np.random.seed([1])
    x, y = np.meshgrid(np.linspace(0, 2.0, n), np.linspace(0, 2.0, n))
    z = np.cos(7 * x) * np.sin(8 * y) + noise_amp * np.random.rand(n, n)
    mask = np.random.rand(n, n) >= mask_level
    z = np.ma.array(z, mask=mask)
    for corner_mask in [False, True]:
        plt.figure(frameon=False)
        plt.contourf(z, corner_mask=corner_mask)
# Mutation info: Added frameon = False (Call plt.figure)