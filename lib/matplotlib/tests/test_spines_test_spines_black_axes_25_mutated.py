import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib.spines import Spines
from matplotlib.testing.decorators import check_figures_equal, image_comparison

@image_comparison(['black_axes'])
def test_spines_black_axes_25_mutated():
    plt.rcParams['savefig.pad_inches'] = 0
    plt.rcParams['savefig.bbox'] = 'tight'
    fig = plt.figure(0, figsize=(4, 4))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([], minor=False)
    ax.set_facecolor((0, 0, 0))
# Mutation info: Added minor = False (Call ax.set_yticks)