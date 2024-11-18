import base64
import io
import platform
import numpy as np
from numpy.testing import assert_array_almost_equal, assert_array_equal
import pytest
from matplotlib.testing.decorators import check_figures_equal, image_comparison, remove_ticks_and_titles
import matplotlib.pyplot as plt
from matplotlib import patches, transforms
from matplotlib.path import Path

@image_comparison(['simplify_curve'], remove_text=True, tol=0.017)
def test_simplify_curve_2_mutated():
    pp1 = patches.PathPatch(Path([(0, 0), (1, 0), (1, 1), (np.nan, 1), (0, 0), (2, 0), (2, 2), (0, 0)], [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY]), fc='none')
    fig, ax = plt.subplots(sharey=True)
    ax.add_patch(pp1)
    ax.set_xlim((0, 2))
    ax.set_ylim((0, 2))
# Mutation info: Added sharey = True (Call plt.subplots)