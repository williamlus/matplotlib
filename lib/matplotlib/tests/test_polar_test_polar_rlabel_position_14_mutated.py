import numpy as np
from numpy.testing import assert_allclose
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

@image_comparison(['polar_rlabel_position'], style='default')
def test_polar_rlabel_position_14_mutated():
    fig = plt.figure()
    ax = fig.add_subplot(projection='polar', polar=True)
    ax.set_rlabel_position(315)
    ax.tick_params(rotation='auto')
# Mutation info: Added polar = True (Call fig.add_subplot)