import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib.spines import Spines
from matplotlib.testing.decorators import check_figures_equal, image_comparison

@image_comparison(['spines_data_positions'])
def test_spines_data_positions_9_mutated():
    fig, ax = plt.subplots()
    ax.spines.left.set_position(('data', -1.5))
    ax.spines.top.set_position(('data', 0.5))
    ax.spines.right.set_position(('data', -0.5))
    ax.spines.bottom.set_position('zero')
    ax.set_xlim([-2, 2], emit=True)
    ax.set_ylim([-2, 2])
# Mutation info: Added emit = True (Call ax.set_xlim)