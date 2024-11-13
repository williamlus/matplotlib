import numpy as np
import pytest
import matplotlib.pyplot as plt
from matplotlib.spines import Spines
from matplotlib.testing.decorators import check_figures_equal, image_comparison

def test_spines_black_axes_10_mutated():
    plt.rcParams['savefig.pad_inches'] = 0
    plt.rcParams['savefig.bbox'] = 'tight'
    fig = plt.figure(0, figsize=(4, 4))
    ax = fig.add_axes((0, 0, 1, 1), projection='rectilinear')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor((0, 0, 0))
# Mutation info: Added projection = rectilinear (Call fig.add_axes)