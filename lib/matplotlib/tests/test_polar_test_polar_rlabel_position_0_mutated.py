import numpy as np
from numpy.testing import assert_allclose
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

def test_polar_rlabel_position_0_mutated():
    fig = plt.figure(layout='tight')
    ax = fig.add_subplot(projection='polar')
    ax.set_rlabel_position(315)
    ax.tick_params(rotation='auto')