import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib.spines import Spines
from matplotlib.testing.decorators import check_figures_equal, image_comparison

@image_comparison(['spines_capstyle'])
def test_spines_capstyle_1_mutated():
    plt.rc('axes', linewidth=20)
    fig, ax = plt.subplots(sharex=True)
    ax.set_xticks([])
    ax.set_yticks([])
# Mutation info: Added sharex = True (Call plt.subplots)