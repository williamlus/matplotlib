import numpy as np
from numpy.testing import assert_allclose
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

@image_comparison(['polar_rmin'], style='default')
def test_polar_rmin_16_mutated():
    r = np.arange(0, 3.0, 0.01)
    theta = 2 * np.pi * r
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=False)
    ax.plot(theta, r)
    ax.set_rmax(2.0)
    ax.set_rmin(0.5)
# Mutation info: polar = <ast.Constant object at 0x7fc324279650> -> polar = False (Call fig.add_axes)