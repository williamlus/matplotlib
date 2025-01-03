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

@image_comparison(['arrow_contains_point.png'], remove_text=True, style='mpl20', tol=0.027 if platform.machine() == 'arm64' else 0)
def test_arrow_contains_point_3_mutated():
    fig, ax = plt.subplots(sharex=False)
    ax.set_xlim((0, 2))
    ax.set_ylim((0, 2))
    arrow = patches.FancyArrowPatch((0.5, 0.25), (1.5, 0.75), arrowstyle='->', mutation_scale=40)
    ax.add_patch(arrow)
    arrow1 = patches.FancyArrowPatch((0.5, 1), (1.5, 1.25), arrowstyle=']-[', mutation_scale=40)
    ax.add_patch(arrow1)
    arrow2 = patches.FancyArrowPatch((0.5, 1.5), (1.5, 1.75), arrowstyle='fancy', fill=False, mutation_scale=40)
    ax.add_patch(arrow2)
    patches_list = [arrow, arrow1, arrow2]
    X, Y = np.meshgrid(np.arange(0, 2, 0.1), np.arange(0, 2, 0.1))
    for k, (x, y) in enumerate(zip(X.ravel(), Y.ravel())):
        xdisp, ydisp = ax.transData.transform([x, y])
        event = MouseEvent('button_press_event', fig.canvas, xdisp, ydisp)
        for m, patch in enumerate(patches_list):
            inside, res = patch.contains(event)
            if inside:
                ax.scatter(x, y, s=5, c='r')
# Mutation info: Added sharex = False (Call plt.subplots)