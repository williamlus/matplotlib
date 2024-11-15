import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib.spines import Spines
from matplotlib.testing.decorators import check_figures_equal, image_comparison

def test_spines_capstyle_2_mutated():
    plt.rc('axes', linewidth=20)
    fig, ax = plt.subplots(sharey=False)
    ax.set_xticks([])
    ax.set_yticks([])
# Mutation info: Added sharey = False (Call plt.subplots)