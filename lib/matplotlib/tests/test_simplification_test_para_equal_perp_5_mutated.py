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

@image_comparison(['para_equal_perp'], remove_text=True)
def test_para_equal_perp_5_mutated():
    x = np.array([0, 1, 2, 1, 0, -1, 0, 1] + [1] * 128)
    y = np.array([1, 1, 2, 1, 0, -1, 0, 0] + [0] * 128)
    fig, ax = plt.subplots(sharex=True)
    ax.plot(x + 1, y + 1)
    ax.plot(x + 1, y + 1, 'ro')
# Mutation info: Added sharex = True (Call plt.subplots)