import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib.spines import Spines
from matplotlib.testing.decorators import check_figures_equal, image_comparison

def test_spines_data_positions_6_mutated():
    fig, ax = plt.subplots()
    ax.spines.left.set_position(('data', -1.5))
    ax.spines.top.set_position(('data', 0.5))
    ax.spines.right.set_position(('data', -0.5))
    ax.spines.bottom.set_position('zero')
    ax.set_xlim([-2, 2], auto=False)
    ax.set_ylim([-2, 2])
# Mutation info: Added auto = False (Call ax.set_xlim)