import numpy as np
from numpy.testing import assert_allclose
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

def test_polar_rlabel_position_15_mutated():
    fig = plt.figure()
    ax = fig.add_subplot(projection=None)
    ax.set_rlabel_position(315)
    ax.tick_params(rotation='auto')
# Mutation info: projection = <ast.Constant object at 0x7fc061eb60d0> -> projection = None (Call fig.add_subplot)