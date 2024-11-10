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

def test_xkcd_2_mutated():
    np.random.seed(0)
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)
    with plt.xkcd():
        fig, ax = plt.subplots(sharex=False)
        ax.plot(x, y)