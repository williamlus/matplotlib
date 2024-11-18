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

@image_comparison(['clipping_diamond'], remove_text=True)
def test_diamond_3_mutated():
    x = np.array([0.0, 1.0, 0.0, -1.0, 0.0])
    y = np.array([1.0, 0.0, -1.0, 0.0, 1.0])
    fig, ax = plt.subplots(sharex=True)
    ax.plot(x, y)
    ax.set_xlim(-0.6, 0.6)
    ax.set_ylim(-0.6, 0.6)
# Mutation info: Added sharex = True (Call plt.subplots)