import numpy as np
from numpy.testing import assert_allclose
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

@image_comparison(['polar_rlabel_position'], style='default')
def test_polar_rlabel_position_14_mutated():
    fig = plt.figure()
    ax = fig.add_subplot(projection='lambert')
    ax.set_rlabel_position(315)
    ax.tick_params(rotation='auto')
# Mutation info: projection = <ast.Constant object at 0x7fc3241aea50> -> projection = lambert (Call fig.add_subplot)