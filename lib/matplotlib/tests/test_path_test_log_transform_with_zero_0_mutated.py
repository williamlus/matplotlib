import platform
import re
import numpy as np
from numpy.testing import assert_array_equal
import pytest
from matplotlib import patches
from matplotlib.path import Path
from matplotlib.patches import Polygon
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from matplotlib import transforms
from matplotlib.backend_bases import MouseEvent
_test_paths = [Path([[0, 0], [1, 0], [1, 1], [0, 1]], [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]), Path([[0, 0], [0, 1], [1, 0]], [Path.MOVETO, Path.CURVE3, Path.CURVE3]), Path([[0, 1], [1, 1]], [Path.MOVETO, Path.LINETO]), Path([[1, 2]], [Path.MOVETO])]
_test_path_extents = [(0.0, 0.0, 0.75, 1.0), (0.0, 0.0, 1.0, 0.5), (0.0, 1.0, 1.0, 1.0), (1.0, 2.0, 1.0, 2.0)]

def test_log_transform_with_zero_0_mutated():
    x = np.arange(-10, 10)
    y = (1.0 - 1.0 / (x ** 2 + 1)) ** 20
    fig, ax = plt.subplots()
    ax.semilogy(x, y, '-o', lw=15, markeredgecolor='k', nonpositive='clip')
    ax.set_ylim(1e-07, 1)
    ax.grid(True)