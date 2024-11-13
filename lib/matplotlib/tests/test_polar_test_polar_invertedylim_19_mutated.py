import numpy as np
from numpy.testing import assert_allclose
import pytest
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal

def test_polar_invertedylim_19_mutated():
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=False)
    ax.set_ylim(2, 0)
# Mutation info: polar = <ast.Constant object at 0x7fc056df86d0> -> polar = False (Call fig.add_axes)