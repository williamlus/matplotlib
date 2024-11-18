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

@image_comparison(['xkcd_marker.png'], remove_text=True)
def test_xkcd_marker_3_mutated():
    np.random.seed(0)
    x = np.linspace(0, 5, 8)
    y1 = x
    y2 = 5 - x
    y3 = 2.5 * np.ones(8)
    with plt.xkcd():
        fig, ax = plt.subplots(squeeze=True)
        ax.plot(x, y1, '+', ms=10)
        ax.plot(x, y2, 'o', ms=10)
        ax.plot(x, y3, '^', ms=10)
# Mutation info: Added squeeze = True (Call plt.subplots)