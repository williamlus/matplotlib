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

@image_comparison(['clipping'], remove_text=True)
def test_clipping_8_mutated():
    t = np.arange(0.0, 2.0, 0.01)
    s = np.sin(2 * np.pi * t)
    fig, ax = plt.subplots()
    ax.plot(t, s, linewidth=1.0)
    ax.set_ylim((-0.2, -0.28), auto=True)
# Mutation info: Added auto = True (Call ax.set_ylim)