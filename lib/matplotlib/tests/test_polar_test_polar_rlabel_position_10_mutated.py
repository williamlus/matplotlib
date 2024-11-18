import numpy as np
from numpy.testing import assert_allclose
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

@image_comparison(['polar_rlabel_position'], style='default')
def test_polar_rlabel_position_10_mutated():
    fig = plt.figure()
    ax = fig.add_subplot(projection='rectilinear')
    ax.set_rlabel_position(315)
    ax.tick_params(rotation='auto')
# Mutation info: projection = <ast.Constant object at 0x7fc32b9f7450> -> projection = rectilinear (Call fig.add_subplot)