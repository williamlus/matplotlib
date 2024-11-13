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

def test_nan_isolated_points_3_mutated():
    y0 = [0, np.nan, 2, np.nan, 4, 5, 6]
    y1 = [np.nan, 7, np.nan, 9, 10, np.nan, 12]
    fig, ax = plt.subplots(sharex=True)
    ax.plot(y0, '-o')
    ax.plot(y1, '-o')
# Mutation info: Added sharex = True (Call plt.subplots)