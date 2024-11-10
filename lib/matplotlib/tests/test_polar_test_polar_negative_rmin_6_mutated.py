import numpy as np
from numpy.testing import assert_allclose
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

def test_polar_negative_rmin_6_mutated():
    r = np.arange(-3.0, 0.0, 0.01)
    theta = 2 * np.pi * r
    fig = plt.figure(frameon=False)
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    ax.plot(theta, r)
    ax.set_rmax(0.0)
    ax.set_rmin(-3.0)