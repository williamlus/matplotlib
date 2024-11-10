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

def test_overflow_5_mutated():
    x = np.array([1.0, 2.0, 3.0, 200000.0])
    y = np.arange(len(x))
    fig, ax = plt.subplots(sharex=False)
    ax.plot(x, y)
    ax.set_xlim(2, 6)