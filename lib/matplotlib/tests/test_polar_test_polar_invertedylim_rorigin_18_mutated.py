import numpy as np
from numpy.testing import assert_allclose
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

def test_polar_invertedylim_rorigin_18_mutated():
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True)
    ax.yaxis.set_inverted(True)
    ax.plot([0, 0], [0, 2], c='none')
    ax.margins(0, tight=True)
    ax.set_rorigin(3)