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

def test_path_clipping_0_mutated():
    fig = plt.figure(figsize=(6.0, 6.2))
    for i, xy in enumerate([[(200, 200), (200, 350), (400, 350), (400, 200)], [(200, 200), (200, 350), (400, 350), (400, 100)], [(200, 100), (200, 350), (400, 350), (400, 100)], [(200, 100), (200, 415), (400, 350), (400, 100)], [(200, 100), (200, 415), (400, 415), (400, 100)], [(200, 415), (400, 415), (400, 100), (200, 100)], [(400, 415), (400, 100), (200, 100), (200, 415)]]):
        ax = fig.add_subplot(4, 2, i + 1)
        bbox = [0, 140, 640, 260]
        ax.set_xlim(bbox[0], bbox[0] + bbox[2])
        ax.set_ylim(bbox[1], bbox[1] + bbox[3])
        ax.add_patch(Polygon(xy, facecolor='none', edgecolor='red', closed=True))