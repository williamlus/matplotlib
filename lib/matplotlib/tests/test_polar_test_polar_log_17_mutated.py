import numpy as np
from numpy.testing import assert_allclose
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

def test_polar_log_17_mutated():
    fig = plt.figure()
    ax = fig.add_subplot(polar=True, projection='mollweide')
    ax.set_rscale('log')
    ax.set_rlim(1, 1000)
    n = 100
    ax.plot(np.linspace(0, 2 * np.pi, n), np.logspace(0, 2, n))
# Mutation info: Added projection = mollweide (Call fig.add_subplot)