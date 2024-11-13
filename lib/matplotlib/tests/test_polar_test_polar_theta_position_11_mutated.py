import numpy as np
from numpy.testing import assert_allclose
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

def test_polar_theta_position_11_mutated():
    r = np.arange(0, 3.0, 0.01)
    theta = 2 * np.pi * r
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True, projection='polar')
    ax.plot(theta, r)
    ax.set_theta_zero_location('NW', 30)
    ax.set_theta_direction('clockwise')
# Mutation info: Added projection = polar (Call fig.add_axes)